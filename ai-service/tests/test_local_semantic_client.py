from llm.local_semantic_client import LocalSemanticClient


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
                            "handler_name": "health",
                            "line_start": 1,
                            "line_end": 3,
                        },
                        {
                            "method": "GET",
                            "path": "/users",
                            "handler_name": "get_users",
                            "line_start": 5,
                            "line_end": 7,
                        },
                    ]
                },
            }
        ],
        "currentEngineeringKnowledge": {
            "readme": {
                "content": """
# User Service

## Endpoints

- GET /health - Health check
""",
            },
            "architectureDocumentation": {
                "content": """
# Architecture

The application is a FastAPI monolith.
""",
            },
            "apiDocumentation": {
                "content": """
# API Documentation

## GET /health

Returns the health status.
""",
            },
        },
    }


def test_detects_undocumented_api_endpoint():
    client = LocalSemanticClient()

    result = client.analyze(build_context())

    readme = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "README"
    )

    architecture = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "ARCHITECTURE"
    )

    api_documentation = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "API_DOCUMENTATION"
    )

    assert readme.driftDetected is True
    assert "/users" in readme.reason

    assert architecture.driftDetected is False

    assert api_documentation.driftDetected is True
    assert "GET /users" in api_documentation.reason


def test_no_drift_when_all_endpoints_are_documented():
    context = build_context()

    context["currentEngineeringKnowledge"]["readme"]["content"] += (
        "\n- GET /users - List users"
    )

    context["currentEngineeringKnowledge"]["apiDocumentation"][
        "content"
    ] += """
    
## GET /users

Returns the list of users.
"""

    client = LocalSemanticClient()

    result = client.analyze(context)

    assert all(
        artifact.driftDetected is False
        for artifact in result.artifacts
    )


def test_returns_no_api_drift_when_no_endpoints_exist():
    context = build_context()

    context["changedCodeFiles"][0]["codeFacts"]["api_endpoints"] = []

    client = LocalSemanticClient()

    result = client.analyze(context)

    api_documentation = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "API_DOCUMENTATION"
    )

    assert api_documentation.driftDetected is False


def test_deduplicates_duplicate_endpoints():
    context = build_context()

    context["changedCodeFiles"][0]["codeFacts"][
        "api_endpoints"
    ].append(
        {
            "method": "GET",
            "path": "/users",
            "handler_name": "get_users_again",
            "line_start": 10,
            "line_end": 12,
        }
    )

    client = LocalSemanticClient()

    result = client.analyze(context)

    api_documentation = next(
        artifact
        for artifact in result.artifacts
        if artifact.artifactType == "API_DOCUMENTATION"
    )

    assert api_documentation.reason.count("GET /users") == 1