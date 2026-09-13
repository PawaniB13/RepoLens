from llm.local_semantic_client import LocalSemanticClient


def build_context(
    architecture_type: str = "monolith",
    architecture_documentation: str = (
        "# Architecture\n\n"
        "The application is implemented as a monolith."
    ),
):
    return {
        "repositoryMetadata": {
            "repositoryId": "repo-1",
            "repositoryName": "user-service",
            "repositoryUrl": "https://github.com/example/user-service",
            "description": "User service",
            "mainTechnologies": ["Python", "FastAPI"],
            "architectureType": architecture_type,
        },
        "changedCodeFiles": [
            {
                "filename": "main.py",
                "language": "python",
                "content": "",
                "codeFacts": {
                    "api_endpoints": [],
                },
            }
        ],
        "currentEngineeringKnowledge": {
            "readme": {
                "content": "",
            },
            "architectureDocumentation": {
                "content": architecture_documentation,
            },
            "apiDocumentation": {
                "content": "",
            },
        },
    }


def test_detects_conflicting_architecture_type():
    context = build_context(
        architecture_type="monolith",
        architecture_documentation=(
            "# Architecture\n\n"
            "The system is implemented using a microservices architecture."
        ),
    )

    result = LocalSemanticClient().analyze(context)

    architecture = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "ARCHITECTURE"
    )

    assert architecture.driftDetected is True
    assert "microservices" in architecture.reason
    assert "monolith" in architecture.reason


def test_no_architecture_drift_when_types_match():
    context = build_context(
        architecture_type="monolith",
        architecture_documentation=(
            "# Architecture\n\n"
            "The application is implemented as a FastAPI monolith."
        ),
    )

    result = LocalSemanticClient().analyze(context)

    architecture = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "ARCHITECTURE"
    )

    assert architecture.driftDetected is False


def test_no_architecture_drift_when_evidence_is_ambiguous():
    context = build_context(
        architecture_type="custom architecture",
        architecture_documentation=(
            "# Architecture\n\n"
            "The application contains several services."
        ),
    )

    result = LocalSemanticClient().analyze(context)

    architecture = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "ARCHITECTURE"
    )

    assert architecture.driftDetected is False
    assert "No deterministic architectural inconsistency" in (
        architecture.reason
    )


def test_no_architecture_drift_when_metadata_is_missing():
    context = build_context(
        architecture_type="",
        architecture_documentation=(
            "# Architecture\n\n"
            "The application is implemented as a monolith."
        ),
    )

    result = LocalSemanticClient().analyze(context)

    architecture = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "ARCHITECTURE"
    )

    assert architecture.driftDetected is False
    assert "metadata is unavailable" in architecture.reason