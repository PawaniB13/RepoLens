from generators.document_update_service import DocumentUpdateService
from generators.engineering_knowledge_update_service import (
    EngineeringKnowledgeUpdateService,
)
from generators.mermaid_extractor import MermaidExtractor
from generators.local_update_client import LocalUpdateClient
from models.requests import (
    ArchitectureDocumentation,
    CurrentEngineeringKnowledge,
    MermaidDiagram,
    ReadmeKnowledge,
    ApiDocumentation,
)
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
                        },
                        {
                            "method": "POST",
                            "path": "/users",
                        },
                    ]
                },
            }
        ],
        "currentEngineeringKnowledge": {
            "readme": {
                "path": "README.md",
                "content": "# User Service",
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
                "content": "# API Documentation",
            },
        },
    }


def build_semantic_analysis():
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
                reason=(
                    "Architecture documentation conflicts with "
                    "repository metadata."
                ),
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


def build_knowledge(context):
    knowledge = context["currentEngineeringKnowledge"]

    return CurrentEngineeringKnowledge(
        readme=ReadmeKnowledge(
            path=knowledge["readme"]["path"],
            content=knowledge["readme"]["content"],
            lastUpdated=None,
        ),
        architectureDocumentation=ArchitectureDocumentation(
            path=knowledge["architectureDocumentation"]["path"],
            content=knowledge["architectureDocumentation"]["content"],
            lastUpdated=None,
            mermaidDiagrams=[
                MermaidDiagram(
                    id="diagram-1",
                    type="mermaid",
                    content=(
                        "flowchart TD\n"
                        "    Client --> ServiceA"
                    ),
                )
            ],
        ),
        apiDocumentation=ApiDocumentation(
            path=knowledge["apiDocumentation"]["path"],
            content=knowledge["apiDocumentation"]["content"],
            lastUpdated=None,
        ),
    )


def test_architecture_update_flows_through_document_update_service():
    context = build_context()
    semantic_analysis = build_semantic_analysis()

    client = LocalUpdateClient()

    updates = client.generate_updates(
        context=context,
        semantic_analysis=semantic_analysis,
    )

    architecture_updates = [
        update
        for update in updates
        if update.artifactType == "ARCHITECTURE"
    ]

    assert len(architecture_updates) == 1

    update = architecture_updates[0]

    knowledge = build_knowledge(context)

    service = EngineeringKnowledgeUpdateService(
        document_update_service=DocumentUpdateService(),
        mermaid_extractor=MermaidExtractor(),
    )

    updated_knowledge = service.apply_updates(
        knowledge=knowledge,
        updates=[update],
    )

    architecture = updated_knowledge.architectureDocumentation

    assert "microservices" not in architecture.content.lower()
    assert "monolith" in architecture.content.lower()

    assert "```mermaid" in architecture.content
    assert "flowchart TD" in architecture.content

    assert len(architecture.mermaidDiagrams) == 1

    diagram = architecture.mermaidDiagrams[0]

    assert diagram.type == "mermaid"
    assert "flowchart TD" in diagram.content


def test_architecture_update_contains_repository_api_facts():
    context = build_context()
    semantic_analysis = build_semantic_analysis()

    updates = LocalUpdateClient().generate_updates(
        context=context,
        semantic_analysis=semantic_analysis,
    )

    architecture_update = next(
        update
        for update in updates
        if update.artifactType == "ARCHITECTURE"
    )

    assert "2 API Endpoints" in architecture_update.suggestedContent