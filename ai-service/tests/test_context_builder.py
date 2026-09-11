from context.context_builder import ContextBuilder
from models.code_facts import CodeFacts
from models.requests import (
    AnalyzeRequest,
    RepositoryMetadata,
    WebhookEvent,
    GitDiff,
    DiffSummary,
    ChangedCodeFile,
    ChangedCodeFiles,
    ReadmeKnowledge,
    ArchitectureDocumentation,
    ApiDocumentation,
    CurrentEngineeringKnowledge,
    PreviousAnalysisMetadata,
)


def create_test_request() -> AnalyzeRequest:
    return AnalyzeRequest(
        repositoryMetadata=RepositoryMetadata(
            repositoryId="123",
            repositoryName="test-repo",
            repositoryUrl="https://github.com/test/test-repo",
            description="Test repository",
            mainTechnologies=["Python"],
            architectureType="REST API",
        ),
        webhookEvent=WebhookEvent(
            type="PULL_REQUEST_MERGED",
            branchName="main",
            previousCommitHash="abc123",
            commitHash="def456",
            commitMessage="Update authentication",
            author="test-user",
            timestamp="2026-08-30T12:00:00Z",
        ),
        gitDiff=GitDiff(
            filesChanged=[],
            summary=DiffSummary(
                totalFilesChanged=1,
                totalLinesAdded=10,
                totalLinesRemoved=2,
            ),
        ),
        changedCodeFiles=ChangedCodeFiles(
            description="Changed source files",
            files=[
                ChangedCodeFile(
                    filename="src/auth.py",
                    language="python",
                    content="def login():\n    pass",
                )
            ],
            maxTotalBytes=None,
        ),
        currentEngineeringKnowledge=CurrentEngineeringKnowledge(
            readme=ReadmeKnowledge(
                path="README.md",
                content="# Test Repository",
                lastUpdated=None,
            ),
            architectureDocumentation=ArchitectureDocumentation(
                path="docs/architecture.md",
                content="System architecture",
                lastUpdated=None,
                mermaidDiagrams=[],
            ),
            apiDocumentation=ApiDocumentation(
                path="docs/api.md",
                content="API documentation",
                lastUpdated=None,
            ),
        ),
        previousAnalysisMetadata=PreviousAnalysisMetadata(
            previousCommitHash=None,
            previousAnalysisTimestamp=None,
            previousDriftDetected=None,
            previousEngineeringTruthScore=None,
        ),
    )


def test_context_builder_preserves_request_data():
    request = create_test_request()

    code_facts = [
        CodeFacts(
            filename="src/auth.py",
            language="python",
            line_count=2,
            file_size_bytes=23,
        )
    ]

    builder = ContextBuilder()

    context = builder.build(
        request=request,
        code_facts=code_facts,
    )

    assert context["repositoryMetadata"]["repositoryId"] == "123"
    assert context["webhookEvent"]["commitHash"] == "def456"

    assert len(context["changedCodeFiles"]) == 1

    changed_file = context["changedCodeFiles"][0]

    assert changed_file["filename"] == "src/auth.py"
    assert changed_file["language"] == "python"
    assert changed_file["content"] == "def login():\n    pass"

    assert changed_file["codeFacts"]["filename"] == "src/auth.py"
    assert changed_file["codeFacts"]["language"] == "python"

    assert (
        context["currentEngineeringKnowledge"]["readme"]["path"]
        == "README.md"
    )

    assert (
        context["previousAnalysisMetadata"]["previousCommitHash"]
        is None
    )


def test_context_builder_handles_multiple_code_files():
    request = create_test_request()

    request.changedCodeFiles.files.append(
        ChangedCodeFile(
            filename="src/user.py",
            language="python",
            content="class User:\n    pass",
        )
    )

    code_facts = [
        CodeFacts(
            filename="src/auth.py",
            language="python",
            line_count=2,
            file_size_bytes=23,
        ),
        CodeFacts(
            filename="src/user.py",
            language="python",
            line_count=2,
            file_size_bytes=19,
        ),
    ]

    builder = ContextBuilder()

    context = builder.build(
        request=request,
        code_facts=code_facts,
    )

    assert len(context["changedCodeFiles"]) == 2

    assert context["changedCodeFiles"][0]["filename"] == "src/auth.py"
    assert context["changedCodeFiles"][1]["filename"] == "src/user.py"


def test_context_builder_handles_empty_code_facts():
    request = create_test_request()

    builder = ContextBuilder()

    context = builder.build(
        request=request,
        code_facts=[],
    )

    assert len(context["changedCodeFiles"]) == 0

    assert context["repositoryMetadata"]["repositoryId"] == "123"
    assert context["webhookEvent"]["commitHash"] == "def456"

    assert "currentEngineeringKnowledge" in context
    assert "previousAnalysisMetadata" in context


def test_context_builder_preserves_file_facts_correspondence():
    request = create_test_request()

    request.changedCodeFiles.files.append(
        ChangedCodeFile(
            filename="src/user.py",
            language="python",
            content="class User:\n    pass",
        )
    )

    code_facts = [
        CodeFacts(
            filename="src/auth.py",
            language="python",
            line_count=2,
            file_size_bytes=23,
        ),
        CodeFacts(
            filename="src/user.py",
            language="python",
            line_count=2,
            file_size_bytes=19,
        ),
    ]

    builder = ContextBuilder()

    context = builder.build(
        request=request,
        code_facts=code_facts,
    )

    assert (
        context["changedCodeFiles"][0]["filename"]
        == context["changedCodeFiles"][0]["codeFacts"]["filename"]
    )

    assert (
        context["changedCodeFiles"][1]["filename"]
        == context["changedCodeFiles"][1]["codeFacts"]["filename"]
    )

    assert (
        context["changedCodeFiles"][0]["language"]
        == context["changedCodeFiles"][0]["codeFacts"]["language"]
    )

    assert (
        context["changedCodeFiles"][1]["language"]
        == context["changedCodeFiles"][1]["codeFacts"]["language"]
    )


def test_context_builder_returns_complete_context_structure():
    request = create_test_request()

    code_facts = [
        CodeFacts(
            filename="src/auth.py",
            language="python",
            line_count=2,
            file_size_bytes=23,
        )
    ]

    builder = ContextBuilder()

    context = builder.build(
        request=request,
        code_facts=code_facts,
    )

    expected_keys = {
        "repositoryMetadata",
        "webhookEvent",
        "gitDiff",
        "changedCodeFiles",
        "currentEngineeringKnowledge",
        "previousAnalysisMetadata",
    }

    assert set(context.keys()) == expected_keys

    assert set(context["repositoryMetadata"].keys()) == set(
        request.repositoryMetadata.model_dump().keys()
    )

    assert set(context["webhookEvent"].keys()) == set(
        request.webhookEvent.model_dump().keys()
    )

    assert set(context["gitDiff"].keys()) == set(
        request.gitDiff.model_dump().keys()
    )

    assert set(context["currentEngineeringKnowledge"].keys()) == set(
        request.currentEngineeringKnowledge.model_dump().keys()
    )

    assert set(context["previousAnalysisMetadata"].keys()) == set(
        request.previousAnalysisMetadata.model_dump().keys()
    )