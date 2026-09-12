from generators.local_update_client import LocalUpdateClient
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)


def build_context():
    return {
        "repositoryMetadata": {
            "architectureType": "monolith",
        },
        "changedCodeFiles": [
            {
                "filename": "main.py",
                "language": "python",
                "content": "",
                "codeFacts": {
                    "api_endpoints": [
                        {
                            "method": "GET",
                            "path": "/users",
                        }
                    ]
                },
            }
        ],
        "currentEngineeringKnowledge": {
            "readme": {
                "path": "README.md",
                "content": "",
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": (
                    "# Architecture\n\n"
                    "The system uses a microservices architecture.\n\n"
                    "```mermaid\n"
                    "flowchart TD\n"
                    "    Client --> ServiceA\n"
                    "```\n"
                ),
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": "",
            },
        },
    }


def architecture_drift():
    return SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=False,
                reason="No README drift.",
                confidence=0.9,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=True,
                reason="Architecture type conflicts.",
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="No API drift.",
                confidence=0.9,
            ),
        ]
    )


def test_generates_architecture_update():
    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=build_context(),
        semantic_analysis=architecture_drift(),
    )

    assert len(updates) == 1

    update = updates[0]

    assert update.artifactType == "ARCHITECTURE"
    assert update.artifactPath == "docs/architecture.md"
    assert update.changeType == "MODIFY"
    assert update.section == "Architecture"
    assert update.currentContent
    assert update.suggestedContent

    assert "monolith" in update.suggestedContent.lower()
    assert "```mermaid" in update.suggestedContent
    assert "flowchart TD" in update.suggestedContent


def test_architecture_update_contains_complete_mermaid_block():
    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=build_context(),
        semantic_analysis=architecture_drift(),
    )

    update = updates[0]

    mermaid_start = update.suggestedContent.find("```mermaid")
    mermaid_end = update.suggestedContent.find(
        "```",
        mermaid_start + len("```mermaid"),
    )

    assert mermaid_start != -1
    assert mermaid_end != -1

    mermaid_content = update.suggestedContent[
        mermaid_start:mermaid_end
    ]

    assert "flowchart TD" in mermaid_content


def test_no_architecture_update_when_architecture_is_not_affected():
    client = LocalUpdateClient()

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README drift.",
                confidence=0.9,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="No architecture drift.",
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="No API drift.",
                confidence=0.9,
            ),
        ]
    )

    updates = client.generate_updates(
        context=build_context(),
        semantic_analysis=semantic_analysis,
    )

    assert all(
        update.artifactType != "ARCHITECTURE"
        for update in updates
    )


def test_no_architecture_update_for_unknown_architecture_type():
    client = LocalUpdateClient()

    context = build_context()
    context["repositoryMetadata"]["architectureType"] = (
        "some unknown architecture"
    )

    updates = client.generate_updates(
        context=context,
        semantic_analysis=architecture_drift(),
    )

    assert updates == []