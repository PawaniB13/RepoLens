from generators.local_update_client import LocalUpdateClient
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)


def build_context():
    return {
        "changedCodeFiles": [
            {
                "filename": "main.py",
                "language": "python",
                "content": "",
                "codeFacts": {
                    "api_endpoints": [
                        {
                            "method": "GET",
                            "path": "/health",
                        },
                        {
                            "method": "GET",
                            "path": "/users",
                        },
                    ]
                },
            }
        ],
        "currentEngineeringKnowledge": {
            "readme": {
                "path": "README.md",
                "content": (
                    "# User Service\n\n"
                    "## API Endpoints\n\n"
                    "- **GET /health** — Health check."
                ),
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": "# Architecture",
                "mermaidDiagrams": [],
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": (
                    "# API Documentation\n\n"
                    "## GET /health\n\n"
                    "Returns the health status."
                ),
            },
        },
    }


def build_semantic_analysis():
    return SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README is missing GET /users.",
                confidence=0.94,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="No architectural drift.",
                confidence=0.85,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=True,
                reason="API documentation is missing GET /users.",
                confidence=0.98,
            ),
        ]
    )


def test_generates_readme_and_api_updates():
    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=build_context(),
        semantic_analysis=build_semantic_analysis(),
    )

    assert len(updates) == 2

    readme_update = next(
        update
        for update in updates
        if update.artifactType == "README"
    )

    api_update = next(
        update
        for update in updates
        if update.artifactType == "API_DOCUMENTATION"
    )

    assert readme_update.changeType == "MODIFY"
    assert "GET /users" in readme_update.suggestedContent
    assert "GET /health" in readme_update.suggestedContent

    assert api_update.changeType == "MODIFY"
    assert "GET /users" in api_update.suggestedContent
    assert "GET /health" in api_update.suggestedContent


def test_does_not_generate_updates_for_non_drifted_artifacts():
    context = build_context()

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=False,
                reason="No README drift.",
                confidence=0.94,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="No architecture drift.",
                confidence=0.85,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="No API documentation drift.",
                confidence=0.98,
            ),
        ]
    )

    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=context,
        semantic_analysis=semantic_analysis,
    )

    assert updates == []


def test_creates_empty_api_documentation():
    context = build_context()

    context["currentEngineeringKnowledge"][
        "apiDocumentation"
    ]["content"] = ""

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=False,
                reason="No README drift.",
                confidence=0.94,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="No architecture drift.",
                confidence=0.85,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=True,
                reason="API documentation is missing GET /users.",
                confidence=0.98,
            ),
        ]
    )

    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=context,
        semantic_analysis=semantic_analysis,
    )

    assert len(updates) == 1

    update = updates[0]

    assert update.artifactType == "API_DOCUMENTATION"
    assert update.changeType == "CREATE"
    assert update.currentContent == ""
    assert "GET /health" in update.suggestedContent
    assert "GET /users" in update.suggestedContent


def test_does_not_duplicate_documented_endpoints():
    context = build_context()

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README drift.",
                confidence=0.94,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="No architecture drift.",
                confidence=0.85,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=True,
                reason="API documentation drift.",
                confidence=0.98,
            ),
        ]
    )

    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=context,
        semantic_analysis=semantic_analysis,
    )

    for update in updates:
        assert update.suggestedContent.count("GET /health") == 1