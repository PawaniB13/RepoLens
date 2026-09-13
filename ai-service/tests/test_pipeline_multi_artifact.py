from generators.llm_update_generator import (
    LLMUpdateGenerator,
    UpdateGenerationClient,
)
from llm.client import LLMClient
from models.requests import AnalyzeRequest
from models.response import SuggestedUpdate
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)
from pipeline.analyzer import AnalysisPipeline


class MultiArtifactLLMClient(LLMClient):
    """Fake semantic-analysis client for multi-artifact testing."""

    def analyze(
        self,
        context: dict,
    ) -> SemanticAnalysisResult:
        return SemanticAnalysisResult(
            artifacts=[
                SemanticArtifactAnalysis(
                    artifactType="README",
                    driftDetected=True,
                    reason="README is missing the new endpoint.",
                    confidence=0.95,
                ),
                SemanticArtifactAnalysis(
                    artifactType="ARCHITECTURE",
                    driftDetected=True,
                    reason="Architecture documentation is outdated.",
                    confidence=0.90,
                ),
                SemanticArtifactAnalysis(
                    artifactType="API_DOCUMENTATION",
                    driftDetected=False,
                    reason="API documentation remains consistent.",
                    confidence=0.95,
                ),
            ]
        )


class MultiArtifactUpdateClient(UpdateGenerationClient):
    """Fake update-generation client for multi-artifact testing."""

    def generate_updates(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        return [
            SuggestedUpdate(
                artifactType="README",
                artifactPath="README.md",
                changeType="MODIFY",
                section="Overview",
                currentContent="A FastAPI application.",
                suggestedContent=(
                    "A FastAPI application.\n\n"
                    "It exposes a GET /hello endpoint."
                ),
                explanation="README does not describe the endpoint.",
                confidence=0.95,
            ),
            SuggestedUpdate(
                artifactType="ARCHITECTURE",
                artifactPath="docs/architecture.md",
                changeType="MODIFY",
                section="Architecture",
                currentContent=(
                    "The application uses FastAPI.\n\n"
                    "```mermaid\n"
                    "flowchart TD\n"
                    "    A[Old Component] --> B[Backend]\n"
                    "```"
                ),
                suggestedContent=(
                    "The application uses FastAPI.\n\n"
                    "```mermaid\n"
                    "flowchart TD\n"
                    "    A[Client] --> B[FastAPI]\n"
                    "    B --> C[Application Logic]\n"
                    "```"
                ),
                explanation=(
                    "The architecture diagram does not represent "
                    "the current application flow."
                ),
                confidence=0.90,
            ),
        ]


def create_request() -> AnalyzeRequest:
    return AnalyzeRequest(
        repositoryMetadata={
            "repositoryId": "repo-multi",
            "repositoryName": "multi-artifact-test",
            "repositoryUrl": (
                "https://github.com/example/multi-artifact-test"
            ),
            "description": "Multi-artifact test repository",
            "mainTechnologies": ["Python", "FastAPI"],
            "architectureType": "monolith",
        },
        webhookEvent={
            "type": "DIRECT_PUSH",
            "branchName": "main",
            "previousCommitHash": "abc123",
            "commitHash": "def456",
            "commitMessage": "Update application",
            "author": "test-user",
            "timestamp": "2026-09-12T10:00:00Z",
        },
        gitDiff={
            "filesChanged": [
                {
                    "filename": "main.py",
                    "status": "MODIFIED",
                    "linesAdded": 5,
                    "linesRemoved": 1,
                    "diffContent": (
                        '+@app.get("/hello")\n'
                        "+def hello():\n"
                        '+    return {"message": "hello"}'
                    ),
                }
            ],
            "summary": {
                "totalFilesChanged": 1,
                "totalLinesAdded": 5,
                "totalLinesRemoved": 1,
            },
        },
        changedCodeFiles={
            "description": "Changed source files",
            "files": [
                {
                    "filename": "main.py",
                    "language": "python",
                    "content": """
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}
""",
                }
            ],
            "maxTotalBytes": 100000,
        },
        currentEngineeringKnowledge={
            "readme": {
                "path": "README.md",
                "content": "A FastAPI application.",
                "lastUpdated": None,
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": (
                    "The application uses FastAPI.\n\n"
                    "```mermaid\n"
                    "flowchart TD\n"
                    "    A[Old Component] --> B[Backend]\n"
                    "```"
                ),
                "lastUpdated": None,
                "mermaidDiagrams": [],
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": "The API is documented.",
                "lastUpdated": None,
            },
        },
        previousAnalysisMetadata={
            "previousCommitHash": None,
            "previousAnalysisTimestamp": None,
            "previousDriftDetected": False,
            "previousEngineeringTruthScore": None,
        },
    )


def test_pipeline_generates_multiple_artifact_updates():
    pipeline = AnalysisPipeline(
        llm_client=MultiArtifactLLMClient(),
        update_generator=LLMUpdateGenerator(
            generation_client=MultiArtifactUpdateClient(),
        ),
    )

    request = create_request()

    result = pipeline.analyze(request)

    assert result.drift_analysis.driftDetected is True

    assert result.drift_analysis.affectedArtifacts == [
        "README",
        "ARCHITECTURE",
    ]

    assert len(result.suggested_updates) == 2

    readme_update = result.suggested_updates[0]

    assert readme_update.artifactType == "README"
    assert readme_update.artifactPath == "README.md"
    assert readme_update.suggestedContent == (
        "A FastAPI application.\n\n"
        "It exposes a GET /hello endpoint."
    )

    architecture_update = result.suggested_updates[1]

    assert architecture_update.artifactType == "ARCHITECTURE"
    assert architecture_update.artifactPath == (
        "docs/architecture.md"
    )
    assert "```mermaid" in architecture_update.suggestedContent
    assert "A[Client] --> B[FastAPI]" in (
        architecture_update.suggestedContent
    )

    # Analysis must not automatically mutate the current
    # engineering knowledge.
    assert request.currentEngineeringKnowledge.readme.content == (
        "A FastAPI application."
    )

    assert (
        request.currentEngineeringKnowledge
        .architectureDocumentation
        .content
        == (
            "The application uses FastAPI.\n\n"
            "```mermaid\n"
            "flowchart TD\n"
            "    A[Old Component] --> B[Backend]\n"
            "```"
        )
    )