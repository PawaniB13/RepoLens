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


class FakeLLMClient(LLMClient):
    """Deterministic LLM client used for pipeline unit tests."""

    def __init__(self) -> None:
        self.received_context = None

    def analyze(
        self,
        context: dict,
    ) -> SemanticAnalysisResult:
        self.received_context = context

        return SemanticAnalysisResult(
            artifacts=[
                SemanticArtifactAnalysis(
                    artifactType="README",
                    driftDetected=True,
                    reason="The README does not describe the new endpoint.",
                    confidence=0.9,
                ),
                SemanticArtifactAnalysis(
                    artifactType="ARCHITECTURE",
                    driftDetected=False,
                    reason="Architecture documentation remains consistent.",
                    confidence=0.95,
                ),
                SemanticArtifactAnalysis(
                    artifactType="API_DOCUMENTATION",
                    driftDetected=False,
                    reason="No API documentation drift was identified.",
                    confidence=0.95,
                ),
            ]
        )


class FakeUpdateGenerationClient(UpdateGenerationClient):
    """Deterministic update-generation client for pipeline tests."""

    def __init__(self) -> None:
        self.called = False
        self.received_context = None
        self.received_semantic_analysis = None

    def generate_updates(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        self.called = True
        self.received_context = context
        self.received_semantic_analysis = semantic_analysis

        return []


def create_request() -> AnalyzeRequest:
    return AnalyzeRequest(
        repositoryMetadata={
            "repositoryId": "repo-1",
            "repositoryName": "test-repository",
            "repositoryUrl": "https://github.com/example/test-repository",
            "description": "Test repository",
            "mainTechnologies": ["Python", "FastAPI"],
            "architectureType": "monolith",
        },
        webhookEvent={
            "type": "DIRECT_PUSH",
            "branchName": "main",
            "previousCommitHash": "abc123",
            "commitHash": "def456",
            "commitMessage": "Add endpoint",
            "author": "test-user",
            "timestamp": "2026-09-12T10:00:00Z",
        },
        gitDiff={
            "filesChanged": [
                {
                    "filename": "main.py",
                    "status": "ADDED",
                    "linesAdded": 5,
                    "linesRemoved": 0,
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
                "totalLinesRemoved": 0,
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
                "content": "This is a FastAPI application.",
                "lastUpdated": None,
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": "The application uses FastAPI.",
                "lastUpdated": None,
                "mermaidDiagrams": [],
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": "",
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


def test_pipeline_orchestrates_analysis_flow():
    fake_llm = FakeLLMClient()

    fake_update_client = FakeUpdateGenerationClient()

    update_generator = LLMUpdateGenerator(
        generation_client=fake_update_client,
    )

    pipeline = AnalysisPipeline(
        llm_client=fake_llm,
        update_generator=update_generator,
    )

    result = pipeline.analyze(create_request())

    assert len(result.code_facts) == 1

    facts = result.code_facts[0]

    assert facts.filename == "main.py"
    assert facts.language == "python"
    assert facts.parse_status == "success"
    assert len(facts.api_endpoints) == 1
    assert facts.api_endpoints[0].method == "GET"
    assert facts.api_endpoints[0].path == "/hello"

    assert fake_llm.received_context is not None

    changed_files = fake_llm.received_context["changedCodeFiles"]

    assert len(changed_files) == 1
    assert changed_files[0]["filename"] == "main.py"
    assert changed_files[0]["codeFacts"]["filename"] == "main.py"

    assert result.semantic_analysis.artifacts[0].driftDetected is True

    assert result.drift_analysis.driftDetected is True
    assert result.drift_analysis.affectedArtifacts == ["README"]
    assert result.drift_analysis.confidence == 0.9

    assert result.suggested_updates == []

    assert fake_update_client.called is True
    assert fake_update_client.received_context is not None
    assert fake_update_client.received_semantic_analysis is not None