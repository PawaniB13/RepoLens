import pytest

from generators.document_update_service import DocumentUpdateService
from generators.engineering_knowledge_update_service import (
    EngineeringKnowledgeUpdateService,
)
from generators.mermaid_extractor import MermaidExtractor
from models.requests import (
    ApiDocumentation,
    ArchitectureDocumentation,
    CurrentEngineeringKnowledge,
    ReadmeKnowledge,
)
from models.response import SuggestedUpdate


def create_knowledge() -> CurrentEngineeringKnowledge:
    return CurrentEngineeringKnowledge(
        readme=ReadmeKnowledge(
            path="README.md",
            content="# RepoLens\n\nOld README content.",
            lastUpdated=None,
        ),
        architectureDocumentation=ArchitectureDocumentation(
            path="docs/architecture.md",
            content=(
                "# Architecture\n\n"
                "Old architecture.\n\n"
                "```mermaid\n"
                "flowchart TD\n"
                "    A[Old Component] --> B[Backend]\n"
                "```"
            ),
            lastUpdated=None,
            mermaidDiagrams=[],
        ),
        apiDocumentation=ApiDocumentation(
            path="docs/api.md",
            content="# API Documentation\n\nOld API documentation.",
            lastUpdated=None,
        ),
    )


def create_service() -> EngineeringKnowledgeUpdateService:
    document_service = DocumentUpdateService()
    mermaid_extractor = MermaidExtractor()

    return EngineeringKnowledgeUpdateService(
        document_update_service=document_service,
        mermaid_extractor=mermaid_extractor,
    )


def create_update(
    artifact_type: str,
    artifact_path: str,
    current_content: str,
    suggested_content: str,
) -> SuggestedUpdate:
    return SuggestedUpdate(
        artifactType=artifact_type,
        artifactPath=artifact_path,
        changeType="MODIFY",
        section="Overview",
        currentContent=current_content,
        suggestedContent=suggested_content,
        explanation="The documentation is outdated.",
        confidence=0.95,
    )


def test_updates_readme_without_changing_other_artifacts():
    service = create_service()

    knowledge = create_knowledge()

    updates = [
        create_update(
            artifact_type="README",
            artifact_path="README.md",
            current_content="Old README content.",
            suggested_content="Updated README content.",
        )
    ]

    result = service.apply_updates(
        knowledge=knowledge,
        updates=updates,
    )

    assert result.readme.content == (
        "# RepoLens\n\nUpdated README content."
    )

    assert result.architectureDocumentation.content == (
        "# Architecture\n\n"
        "Old architecture.\n\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    A[Old Component] --> B[Backend]\n"
        "```"
    )

    assert result.apiDocumentation.content == (
        "# API Documentation\n\nOld API documentation."
    )


def test_updates_multiple_artifacts():
    service = create_service()

    knowledge = create_knowledge()

    updates = [
        create_update(
            artifact_type="README",
            artifact_path="README.md",
            current_content="Old README content.",
            suggested_content="Updated README content.",
        ),
        create_update(
            artifact_type="ARCHITECTURE",
            artifact_path="docs/architecture.md",
            current_content=(
                "Old architecture.\n\n"
                "```mermaid\n"
                "flowchart TD\n"
                "    A[Old Component] --> B[Backend]\n"
                "```"
            ),
            suggested_content=(
                "Updated architecture.\n\n"
                "```mermaid\n"
                "flowchart TD\n"
                "    A[Frontend] --> B[Backend]\n"
                "    B --> C[AI Service]\n"
                "```"
            ),
        ),
        create_update(
            artifact_type="API_DOCUMENTATION",
            artifact_path="docs/api.md",
            current_content="Old API documentation.",
            suggested_content="Updated API documentation.",
        ),
    ]

    result = service.apply_updates(
        knowledge=knowledge,
        updates=updates,
    )

    assert result.readme.content == (
        "# RepoLens\n\nUpdated README content."
    )

    assert result.architectureDocumentation.content == (
        "# Architecture\n\n"
        "Updated architecture.\n\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    A[Frontend] --> B[Backend]\n"
        "    B --> C[AI Service]\n"
        "```"
    )

    assert result.apiDocumentation.content == (
        "# API Documentation\n\nUpdated API documentation."
    )


def test_rejects_update_for_unknown_artifact_type():
    service = create_service()

    knowledge = create_knowledge()

    update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    update.artifactType = "UNKNOWN"

    with pytest.raises(
        ValueError,
        match="Unsupported engineering knowledge artifact",
    ):
        service.apply_updates(
            knowledge=knowledge,
            updates=[update],
        )


def test_rebuilds_mermaid_metadata_after_architecture_update():
    service = create_service()

    knowledge = create_knowledge()

    update = create_update(
        artifact_type="ARCHITECTURE",
        artifact_path="docs/architecture.md",
        current_content=(
            "Old architecture.\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            "    A[Old Component] --> B[Backend]\n"
            "```"
        ),
        suggested_content=(
            "Updated architecture.\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            "    A[Frontend] --> B[Backend]\n"
            "    B --> C[AI Service]\n"
            "```"
        ),
    )

    result = service.apply_updates(
        knowledge=knowledge,
        updates=[update],
    )

    assert result.architectureDocumentation.content == (
        "# Architecture\n\n"
        "Updated architecture.\n\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    A[Frontend] --> B[Backend]\n"
        "    B --> C[AI Service]\n"
        "```"
    )

    diagrams = result.architectureDocumentation.mermaidDiagrams

    assert len(diagrams) == 1

    assert diagrams[0].id == "diagram-1"
    assert diagrams[0].type == "mermaid"
    assert diagrams[0].content == (
        "flowchart TD\n"
        "    A[Frontend] --> B[Backend]\n"
        "    B --> C[AI Service]"
    )


def test_rebuilds_multiple_mermaid_diagrams_after_architecture_update():
    service = create_service()

    knowledge = create_knowledge()

    update = create_update(
        artifact_type="ARCHITECTURE",
        artifact_path="docs/architecture.md",
        current_content=(
            "Old architecture.\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            "    A[Old Component] --> B[Backend]\n"
            "```"
        ),
        suggested_content=(
            "Updated architecture.\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            "    A[Frontend] --> B[Backend]\n"
            "```\n\n"
            "```mermaid\n"
            "sequenceDiagram\n"
            "    Client->>Server: Request\n"
            "    Server-->>Client: Response\n"
            "```"
        ),
    )

    result = service.apply_updates(
        knowledge=knowledge,
        updates=[update],
    )

    diagrams = result.architectureDocumentation.mermaidDiagrams

    assert len(diagrams) == 2

    assert diagrams[0].id == "diagram-1"
    assert diagrams[0].type == "mermaid"
    assert diagrams[0].content == (
        "flowchart TD\n"
        "    A[Frontend] --> B[Backend]"
    )

    assert diagrams[1].id == "diagram-2"
    assert diagrams[1].type == "mermaid"
    assert diagrams[1].content == (
        "sequenceDiagram\n"
        "    Client->>Server: Request\n"
        "    Server-->>Client: Response"
    )


def test_non_architecture_update_does_not_rebuild_mermaid_metadata():
    service = create_service()

    knowledge = create_knowledge()

    original_diagrams = knowledge.architectureDocumentation.mermaidDiagrams

    update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    result = service.apply_updates(
        knowledge=knowledge,
        updates=[update],
    )

    assert result.architectureDocumentation.mermaidDiagrams == (
        original_diagrams
    )

    