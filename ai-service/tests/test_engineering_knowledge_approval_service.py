import pytest

from generators.document_update_service import DocumentUpdateService
from generators.engineering_knowledge_approval_service import (
    EngineeringKnowledgeApprovalService,
)
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


def create_service() -> EngineeringKnowledgeApprovalService:
    update_service = EngineeringKnowledgeUpdateService(
        document_update_service=DocumentUpdateService(),
        mermaid_extractor=MermaidExtractor(),
    )

    return EngineeringKnowledgeApprovalService(
        update_service=update_service,
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


def test_approved_readme_update_is_applied():
    service = create_service()
    knowledge = create_knowledge()

    update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    result = service.apply_approved_updates(
        knowledge=knowledge,
        suggested_updates=[update],
        approved_updates=[update],
    )

    assert result.readme.content == (
        "# RepoLens\n\nUpdated README content."
    )

    assert result.apiDocumentation.content == (
        "# API Documentation\n\nOld API documentation."
    )


def test_ignored_update_leaves_document_unchanged():
    service = create_service()
    knowledge = create_knowledge()

    update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    result = service.apply_approved_updates(
        knowledge=knowledge,
        suggested_updates=[update],
        approved_updates=[],
    )

    assert result.readme.content == (
        "# RepoLens\n\nOld README content."
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


def test_only_approved_update_is_applied_when_some_are_ignored():
    service = create_service()
    knowledge = create_knowledge()

    readme_update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    api_update = create_update(
        artifact_type="API_DOCUMENTATION",
        artifact_path="docs/api.md",
        current_content="Old API documentation.",
        suggested_content="Updated API documentation.",
    )

    result = service.apply_approved_updates(
        knowledge=knowledge,
        suggested_updates=[readme_update, api_update],
        approved_updates=[readme_update],
    )

    assert result.readme.content == (
        "# RepoLens\n\nUpdated README content."
    )

    assert result.apiDocumentation.content == (
        "# API Documentation\n\nOld API documentation."
    )


def test_all_approved_updates_are_applied():
    service = create_service()
    knowledge = create_knowledge()

    readme_update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    api_update = create_update(
        artifact_type="API_DOCUMENTATION",
        artifact_path="docs/api.md",
        current_content="Old API documentation.",
        suggested_content="Updated API documentation.",
    )

    result = service.apply_approved_updates(
        knowledge=knowledge,
        suggested_updates=[readme_update, api_update],
        approved_updates=[readme_update, api_update],
    )

    assert result.readme.content == (
        "# RepoLens\n\nUpdated README content."
    )

    assert result.apiDocumentation.content == (
        "# API Documentation\n\nUpdated API documentation."
    )


def test_rejects_approval_for_unknown_suggestion():
    service = create_service()
    knowledge = create_knowledge()

    generated_update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Updated README content.",
    )

    unknown_update = create_update(
        artifact_type="README",
        artifact_path="README.md",
        current_content="Old README content.",
        suggested_content="Completely different content.",
    )

    with pytest.raises(
        ValueError,
        match="not present in the generated suggested updates",
    ):
        service.apply_approved_updates(
            knowledge=knowledge,
            suggested_updates=[generated_update],
            approved_updates=[unknown_update],
        )


def test_approved_architecture_update_rebuilds_mermaid_metadata():
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

    result = service.apply_approved_updates(
        knowledge=knowledge,
        suggested_updates=[update],
        approved_updates=[update],
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

    assert len(
        result.architectureDocumentation.mermaidDiagrams
    ) == 1

    assert (
        result.architectureDocumentation.mermaidDiagrams[0].content
        == (
            "flowchart TD\n"
            "    A[Frontend] --> B[Backend]\n"
            "    B --> C[AI Service]"
        )
    )