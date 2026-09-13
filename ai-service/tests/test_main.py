from fastapi.testclient import TestClient

from drift.detector import DriftDetector
from exceptions import AnalysisFailedException
from main import app, get_analysis_pipeline
from models.response import SuggestedUpdate
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)
from pipeline.analyzer import PipelineAnalysisResult


class FakeAnalysisPipeline:
    """Deterministic pipeline used for API tests."""

    def __init__(self, drift_detected: bool = True):
        self.drift_detected = drift_detected

    def analyze(self, request):
        semantic_analysis = SemanticAnalysisResult(
            artifacts=[
                SemanticArtifactAnalysis(
                    artifactType="README",
                    driftDetected=self.drift_detected,
                    reason=(
                        "README describes outdated behavior."
                        if self.drift_detected
                        else "README remains consistent."
                    ),
                    confidence=0.95,
                ),
                SemanticArtifactAnalysis(
                    artifactType="ARCHITECTURE",
                    driftDetected=False,
                    reason="Architecture remains consistent.",
                    confidence=0.90,
                ),
                SemanticArtifactAnalysis(
                    artifactType="API_DOCUMENTATION",
                    driftDetected=False,
                    reason="API documentation remains consistent.",
                    confidence=0.92,
                ),
            ]
        )

        drift_analysis = DriftDetector().detect(
            semantic_analysis=semantic_analysis
        )

        suggested_updates = []

        if self.drift_detected:
            suggested_updates.append(
                SuggestedUpdate(
                    artifactType="README",
                    artifactPath="README.md",
                    changeType="MODIFY",
                    section="Authentication",
                    currentContent=(
                        "The application uses JWT authentication."
                    ),
                    suggestedContent=(
                        "The application uses OAuth2 authentication."
                    ),
                    explanation=(
                        "Authentication documentation is outdated."
                    ),
                    confidence=0.95,
                )
            )

        return PipelineAnalysisResult(
            code_facts=[],
            semantic_analysis=semantic_analysis,
            drift_analysis=drift_analysis,
            suggested_updates=suggested_updates,
        )


def build_request_payload():
    """Build a valid AnalyzeRequest payload for API tests."""

    return {
        "repositoryMetadata": {
            "repositoryId": "repo-123",
            "repositoryName": "test-repository",
            "repositoryUrl": (
                "https://github.com/example/test-repository"
            ),
            "description": "Test repository",
            "mainTechnologies": [
                "Python",
                "FastAPI",
            ],
            "architectureType": "Monolith",
        },
        "webhookEvent": {
            "type": "DIRECT_PUSH",
            "branchName": "main",
            "previousCommitHash": "abc123",
            "commitHash": "def456",
            "commitMessage": "Update authentication",
            "author": "test-user",
            "timestamp": "2026-09-12T10:00:00Z",
        },
        "gitDiff": {
            "filesChanged": [],
            "summary": {
                "totalFilesChanged": 0,
                "totalLinesAdded": 0,
                "totalLinesRemoved": 0,
            },
        },
        "changedCodeFiles": {
            "description": "Changed source files",
            "files": [],
            "maxTotalBytes": None,
        },
        "currentEngineeringKnowledge": {
            "readme": {
                "path": "README.md",
                "content": "Test README",
                "lastUpdated": None,
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": "Test architecture",
                "lastUpdated": None,
                "mermaidDiagrams": [],
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": "Test API documentation",
                "lastUpdated": None,
            },
        },
        "previousAnalysisMetadata": {
            "previousCommitHash": None,
            "previousAnalysisTimestamp": None,
            "previousDriftDetected": None,
            "previousEngineeringTruthScore": None,
        },
    }


def test_root_endpoint():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "RepoLens AI Service is running!"
    }


def test_analyze_endpoint_uses_analysis_pipeline():
    fake_pipeline = FakeAnalysisPipeline(
        drift_detected=True
    )

    app.dependency_overrides[get_analysis_pipeline] = (
        lambda: fake_pipeline
    )

    try:
        response = TestClient(app).post(
            "/api/v1/analyze",
            json=build_request_payload(),
        )

        assert response.status_code == 200

        body = response.json()

        assert body["analysisMetadata"]["repositoryId"] == "repo-123"
        assert body["analysisMetadata"]["commitHash"] == "def456"

        assert body["driftAnalysis"]["driftDetected"] is True
        assert body["driftAnalysis"]["affectedArtifacts"] == [
            "README"
        ]

        assert len(body["suggestedUpdates"]) == 1
        assert body["suggestedUpdates"][0]["artifactType"] == "README"

        # The public API exposes suggestions only.
        assert "updatedEngineeringKnowledge" not in body

    finally:
        app.dependency_overrides.clear()


def test_analyze_endpoint_rejects_invalid_request():
    client = TestClient(app)

    response = client.post(
        "/api/v1/analyze",
        json={},
    )

    assert response.status_code == 422


def test_analyze_endpoint_returns_no_change_when_no_drift():
    fake_pipeline = FakeAnalysisPipeline(
        drift_detected=False
    )

    app.dependency_overrides[get_analysis_pipeline] = (
        lambda: fake_pipeline
    )

    try:
        response = TestClient(app).post(
            "/api/v1/analyze",
            json=build_request_payload(),
        )

        assert response.status_code == 200

        body = response.json()

        assert body["driftAnalysis"]["driftDetected"] is False
        assert body["driftAnalysis"]["affectedArtifacts"] == []
        assert body["suggestedUpdates"] == []
        assert body["noChangeReason"]

    finally:
        app.dependency_overrides.clear()


def test_analyze_endpoint_returns_analysis_failed_error():
    class FailingPipeline:
        def analyze(self, request):
            raise AnalysisFailedException(
                message="Repository analysis could not be completed.",
                failed_files=["src/main.py"],
                reason="The source file could not be analyzed.",
            )

    app.dependency_overrides[get_analysis_pipeline] = (
        lambda: FailingPipeline()
    )

    try:
        response = TestClient(app).post(
            "/api/v1/analyze",
            json=build_request_payload(),
        )

        assert response.status_code == 422

        body = response.json()

        assert body["error"] == "ANALYSIS_FAILED"
        assert body["message"] == (
            "Repository analysis could not be completed."
        )
        assert body["details"]["failedFiles"] == [
            "src/main.py"
        ]
        assert body["details"]["reason"] == (
            "The source file could not be analyzed."
        )

    finally:
        app.dependency_overrides.clear()


def test_analyze_endpoint_returns_internal_server_error():
    class BrokenPipeline:
        def analyze(self, request):
            raise RuntimeError("Unexpected internal failure")

    app.dependency_overrides[get_analysis_pipeline] = (
        lambda: BrokenPipeline()
    )

    try:
        response = TestClient(
            app,
            raise_server_exceptions=False,
        ).post(
            "/api/v1/analyze",
            json=build_request_payload(),
        )

        assert response.status_code == 500

        body = response.json()

        assert body["error"] == "INTERNAL_ERROR"
        assert body["message"] == (
            "An unexpected internal error occurred."
        )

    finally:
        app.dependency_overrides.clear()