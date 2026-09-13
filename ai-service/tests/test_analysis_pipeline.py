from models.response import SuggestedUpdate
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)
from pipeline.analyzer import AnalysisPipeline


class FakeLLMClient:
    """Deterministic fake semantic-analysis client for pipeline tests."""

    def __init__(self, semantic_result: SemanticAnalysisResult):
        self.semantic_result = semantic_result
        self.received_context = None
        self.call_count = 0

    def analyze(self, context: dict) -> SemanticAnalysisResult:
        self.call_count += 1
        self.received_context = context

        return self.semantic_result


class FakeUpdateGenerator:
    """Deterministic fake update generator for pipeline tests."""

    def __init__(self, updates: list[SuggestedUpdate]):
        self.updates = updates
        self.received_context = None
        self.received_semantic_analysis = None
        self.call_count = 0

    def generate(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        self.call_count += 1
        self.received_context = context
        self.received_semantic_analysis = semantic_analysis

        return self.updates


def create_request():
    # Importing here keeps the test fixture focused and avoids
    # unnecessary module-level setup.
    from models.requests import (
        AnalyzeRequest,
        ApiDocumentation,
        ArchitectureDocumentation,
        ChangedCodeFile,
        ChangedCodeFiles,
        ChangedFile,
        CurrentEngineeringKnowledge,
        DiffSummary,
        GitDiff,
        ReadmeKnowledge,
        RepositoryMetadata,
        WebhookEvent,
    )

    return AnalyzeRequest(
        repositoryMetadata=RepositoryMetadata(
            repositoryId="repo-123",
            repositoryName="RepoLens",
            repositoryUrl="https://github.com/example/repolens",
            description="Repository analysis service.",
            mainTechnologies=["Python", "FastAPI"],
            architectureType="Service-based",
        ),
        webhookEvent=WebhookEvent(
            type="PULL_REQUEST_MERGED",
            branchName="main",
            previousCommitHash="abc123",
            commitHash="def456",
            commitMessage="Add analysis endpoint",
            author="developer",
            timestamp="2026-09-12T12:00:00Z",
        ),
        gitDiff=GitDiff(
            filesChanged=[
                ChangedFile(
                    filename="app.py",
                    status="MODIFIED",
                    linesAdded=10,
                    linesRemoved=2,
                    diffContent="+new code",
                )
            ],
            summary=DiffSummary(
                totalFilesChanged=1,
                totalLinesAdded=10,
                totalLinesRemoved=2,
            ),
        ),
        changedCodeFiles=ChangedCodeFiles(
            description="Changed source files.",
            files=[
                ChangedCodeFile(
                    filename="app.py",
                    language="python",
                    content=(
                        "class App:\n"
                        "    def run(self):\n"
                        "        return True\n"
                    ),
                )
            ],
            maxTotalBytes=None,
        ),
        currentEngineeringKnowledge=CurrentEngineeringKnowledge(
            readme=ReadmeKnowledge(
                path="README.md",
                content="# RepoLens",
                lastUpdated=None,
            ),
            architectureDocumentation=ArchitectureDocumentation(
                path="docs/architecture.md",
                content="# Architecture",
                lastUpdated=None,
                mermaidDiagrams=[],
            ),
            apiDocumentation=ApiDocumentation(
                path="docs/api.md",
                content="# API",
                lastUpdated=None,
            ),
        ),
        previousAnalysisMetadata={
            "previousCommitHash": None,
            "previousAnalysisTimestamp": None,
            "previousDriftDetected": None,
            "previousEngineeringTruthScore": None,
        },
    )


def create_semantic_result(
    drift_detected: bool = False,
) -> SemanticAnalysisResult:
    return SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=drift_detected,
                reason=(
                    "README describes the repository correctly."
                    if not drift_detected
                    else "README no longer reflects the current repository."
                ),
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="Architecture remains accurate.",
                confidence=0.90,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation remains accurate.",
                confidence=0.92,
            ),
        ]
    )


def test_pipeline_executes_all_analysis_stages():
    semantic_result = create_semantic_result()

    llm_client = FakeLLMClient(
        semantic_result=semantic_result,
    )

    update_generator = FakeUpdateGenerator(
        updates=[],
    )

    pipeline = AnalysisPipeline(
        llm_client=llm_client,
        update_generator=update_generator,
    )

    result = pipeline.analyze(
        request=create_request(),
    )

    assert len(result.code_facts) == 1

    assert result.code_facts[0].filename == "app.py"
    assert result.code_facts[0].parse_status == "success"

    assert result.semantic_analysis == semantic_result

    assert result.drift_analysis.driftDetected is False
    assert result.drift_analysis.affectedArtifacts == []

    assert result.suggested_updates == []

    assert llm_client.call_count == 1
    assert update_generator.call_count == 1


def test_pipeline_passes_structured_context_to_llm():
    semantic_result = create_semantic_result()

    llm_client = FakeLLMClient(
        semantic_result=semantic_result,
    )

    update_generator = FakeUpdateGenerator(
        updates=[],
    )

    pipeline = AnalysisPipeline(
        llm_client=llm_client,
        update_generator=update_generator,
    )

    pipeline.analyze(
        request=create_request(),
    )

    context = llm_client.received_context

    assert context is not None

    assert context["repositoryMetadata"]["repositoryId"] == (
        "repo-123"
    )

    assert context["webhookEvent"]["commitHash"] == (
        "def456"
    )

    assert len(context["changedCodeFiles"]) == 1

    assert context["changedCodeFiles"][0]["filename"] == (
        "app.py"
    )

    assert context["changedCodeFiles"][0]["codeFacts"]["parse_status"] == (
        "success"
    )


def test_pipeline_preserves_one_code_fact_per_changed_file():
    from models.requests import ChangedCodeFile

    request = create_request()

    request.changedCodeFiles.files.append(
        ChangedCodeFile(
            filename="utils.py",
            language="python",
            content=(
                "def helper():\n"
                "    return 42\n"
            ),
        )
    )

    semantic_result = create_semantic_result()

    llm_client = FakeLLMClient(
        semantic_result=semantic_result,
    )

    update_generator = FakeUpdateGenerator(
        updates=[],
    )

    pipeline = AnalysisPipeline(
        llm_client=llm_client,
        update_generator=update_generator,
    )

    result = pipeline.analyze(
        request=request,
    )

    assert len(result.code_facts) == 2

    assert result.code_facts[0].filename == "app.py"
    assert result.code_facts[1].filename == "utils.py"

    assert (
        llm_client.received_context["changedCodeFiles"][0]["filename"]
        == "app.py"
    )

    assert (
        llm_client.received_context["changedCodeFiles"][1]["filename"]
        == "utils.py"
    )


def test_pipeline_propagates_drift_and_suggested_updates():
    semantic_result = create_semantic_result(
        drift_detected=True,
    )

    update = SuggestedUpdate(
        artifactType="README",
        artifactPath="README.md",
        changeType="MODIFY",
        section="Overview",
        currentContent="# RepoLens",
        suggestedContent=(
            "# RepoLens\n\n"
            "Updated repository description."
        ),
        explanation=(
            "The README no longer reflects the current repository."
        ),
        confidence=0.94,
    )

    llm_client = FakeLLMClient(
        semantic_result=semantic_result,
    )

    update_generator = FakeUpdateGenerator(
        updates=[update],
    )

    pipeline = AnalysisPipeline(
        llm_client=llm_client,
        update_generator=update_generator,
    )

    result = pipeline.analyze(
        request=create_request(),
    )

    assert result.drift_analysis.driftDetected is True

    assert result.drift_analysis.affectedArtifacts == [
        "README"
    ]

    assert len(result.suggested_updates) == 1

    assert result.suggested_updates[0] == update

    assert update_generator.call_count == 1

    assert (
        update_generator.received_semantic_analysis
        == semantic_result
    )
    