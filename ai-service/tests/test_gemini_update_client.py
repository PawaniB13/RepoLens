import os

import pytest
from dotenv import load_dotenv

from llm.config import LLMConfig
from llm.gemini_client import GeminiClient
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)

load_dotenv()


def create_config() -> LLMConfig:
    api_key = os.getenv("GEMINI_API_KEY", "test-api-key")

    return LLMConfig(
        provider="gemini",
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        ),
        api_key=api_key,
        timeout_seconds=30,
        max_retries=2,
    )


def create_context() -> dict:
    return {
        "repositoryMetadata": {
            "repositoryId": "test-repo",
            "repositoryName": "RepoLens",
            "repositoryUrl": "https://github.com/example/repolens",
            "description": "Repository analysis service.",
            "mainTechnologies": ["Python", "FastAPI"],
            "architectureType": "Service-based",
        },
        "webhookEvent": {
            "type": "PULL_REQUEST_MERGED",
            "branchName": "main",
            "previousCommitHash": "abc123",
            "commitHash": "def456",
            "commitMessage": "Update service",
            "author": "developer",
            "timestamp": "2026-09-12T12:00:00Z",
        },
        "gitDiff": {
            "filesChanged": [],
            "summary": {
                "totalFilesChanged": 0,
                "totalLinesAdded": 0,
                "totalLinesRemoved": 0,
            },
        },
        "changedCodeFiles": [],
        "currentEngineeringKnowledge": {
            "readme": {
                "path": "README.md",
                "content": "# RepoLens",
                "lastUpdated": None,
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": "# Architecture",
                "lastUpdated": None,
                "mermaidDiagrams": [],
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": "# API",
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


def test_gemini_returns_valid_semantic_analysis():
    if os.getenv("RUN_LLM_INTEGRATION_TESTS") != "1":
        pytest.skip(
            "Real Gemini integration test disabled. "
            "Set RUN_LLM_INTEGRATION_TESTS=1 to run it."
        )

    client = GeminiClient(create_config())

    result = client.analyze(create_context())

    assert isinstance(result, SemanticAnalysisResult)

    assert len(result.artifacts) == 3

    artifact_types = {
        artifact.artifactType
        for artifact in result.artifacts
    }

    assert artifact_types == {
        "README",
        "ARCHITECTURE",
        "API_DOCUMENTATION",
    }

    for artifact in result.artifacts:
        assert artifact.reason.strip()
        assert 0 <= artifact.confidence <= 1


def test_gemini_rejects_empty_response(monkeypatch):
    client = GeminiClient(create_config())

    class FakeInteraction:
        output_text = ""

    monkeypatch.setattr(
        client.client.interactions,
        "create",
        lambda **kwargs: FakeInteraction(),
    )

    with pytest.raises(
        ValueError,
        match="Gemini returned an empty response",
    ):
        client.analyze(create_context())


def test_gemini_rejects_invalid_json(monkeypatch):
    client = GeminiClient(create_config())

    class FakeInteraction:
        output_text = "this is not valid json"

    monkeypatch.setattr(
        client.client.interactions,
        "create",
        lambda **kwargs: FakeInteraction(),
    )

    with pytest.raises(
        ValueError,
        match="Invalid JSON|validation",
    ):
        client.analyze(create_context())


def test_gemini_rejects_schema_invalid_response(monkeypatch):
    client = GeminiClient(create_config())

    class FakeInteraction:
        output_text = """
        {
            "artifacts": [
                {
                    "artifactType": "README",
                    "driftDetected": true,
                    "reason": "README is outdated.",
                    "confidence": 2.0
                }
            ]
        }
        """

    monkeypatch.setattr(
        client.client.interactions,
        "create",
        lambda **kwargs: FakeInteraction(),
    )

    with pytest.raises(Exception):
        client.analyze(create_context())


def test_semantic_analysis_model_rejects_invalid_confidence():
    with pytest.raises(Exception):
        SemanticArtifactAnalysis(
            artifactType="README",
            driftDetected=True,
            reason="Invalid confidence.",
            confidence=2.0,
        )


def test_semantic_analysis_model_accepts_valid_confidence():
    result = SemanticArtifactAnalysis(
        artifactType="README",
        driftDetected=True,
        reason="README is outdated.",
        confidence=0.95,
    )

    assert result.confidence == 0.95


def test_semantic_analysis_result_requires_artifacts():
    result = SemanticAnalysisResult(
        artifacts=[]
    )

    assert result.artifacts == []