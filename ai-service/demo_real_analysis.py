from pprint import pprint

from application.pipeline_factory import create_analysis_pipeline
from models.requests import AnalyzeRequest


def build_demo_request() -> AnalyzeRequest:
    return AnalyzeRequest(
        repositoryMetadata={
            "repositoryId": "demo-repository",
            "repositoryName": "user-service",
            "repositoryUrl": "https://github.com/example/user-service",
            "description": "A FastAPI service for managing users.",
            "mainTechnologies": ["Python", "FastAPI"],
            "architectureType": "Monolith",
        },
        webhookEvent={
            "type": "DIRECT_PUSH",
            "branchName": "main",
            "previousCommitHash": "abc123",
            "commitHash": "def456",
            "commitMessage": "Add users endpoint",
            "author": "demo-user",
            "timestamp": "2026-09-13T00:00:00Z",
        },
        gitDiff={
            "filesChanged": [
                {
                    "filename": "main.py",
                    "status": "MODIFIED",
                    "linesAdded": 4,
                    "linesRemoved": 0,
                    "diffContent": (
                        '+@app.get("/users")\n'
                        "+def get_users():\n"
                        '+    return {"users": []}'
                    ),
                }
            ],
            "summary": {
                "totalFilesChanged": 1,
                "totalLinesAdded": 4,
                "totalLinesRemoved": 0,
            },
        },
        changedCodeFiles={
            "description": "Source files changed by the latest commit.",
            "files": [
                {
                    "filename": "main.py",
                    "language": "python",
                    "content": """
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def get_users():
    return {"users": []}
""".strip(),
                }
            ],
            "maxTotalBytes": 100000,
        },
        currentEngineeringKnowledge={
            "readme": {
                "path": "README.md",
                "content": """
# User Service

A FastAPI service for managing users.

## Endpoints

- GET /health - Health check
""".strip(),
                "lastUpdated": None,
            },
            "architectureDocumentation": {
                "path": "docs/architecture.md",
                "content": """
# Architecture

The application is implemented using a microservices architecture.

```mermaid
flowchart TD
    Client --> UserService
    Client --> AuthService
    UserService --> UserDatabase
    AuthService --> AuthDatabase
```
""".strip(),
                "lastUpdated": None,
                "mermaidDiagrams": [
                    {
                        "id": "diagram-1",
                        "type": "mermaid",
                        "content": (
                            "flowchart TD\n"
                            "    Client --> UserService\n"
                            "    Client --> AuthService\n"
                            "    UserService --> UserDatabase\n"
                            "    AuthService --> AuthDatabase"
                        ),
                    }
                ],
            },
            "apiDocumentation": {
                "path": "docs/api.md",
                "content": """
# API Documentation

## GET /health

Returns the health status of the service.
""".strip(),
                "lastUpdated": None,
            },
        },
        previousAnalysisMetadata={
            "previousCommitHash": "abc123",
            "previousAnalysisTimestamp": "2026-09-12T23:00:00Z",
            "previousDriftDetected": False,
            "previousEngineeringTruthScore": 0.95,
        },
    )


def main() -> None:
    print("=" * 70)
    print("RepoLens - REAL AI ANALYSIS DEMO")
    print("=" * 70)

    print("\nCreating analysis pipeline...")
    pipeline = create_analysis_pipeline()

    print("Running RepoLens analysis...")
    print("This may take a few seconds...\n")

    result = pipeline.analyze(build_demo_request())

    print("=" * 70)
    print("DRIFT ANALYSIS")
    print("=" * 70)

    pprint(
        result.drift_analysis.model_dump(),
        sort_dicts=False,
    )

    print("\n" + "=" * 70)
    print("SUGGESTED UPDATES")
    print("=" * 70)

    if not result.suggested_updates:
        print("No updates suggested.")
    else:
        for index, update in enumerate(
            result.suggested_updates,
            start=1,
        ):
            print(f"\n--- Update {index} ---")
            pprint(
                update.model_dump(),
                sort_dicts=False,
            )

    print("\n" + "=" * 70)
    print("DETERMINISTIC CODE FACTS")
    print("=" * 70)

    for facts in result.code_facts:
        print(f"\nFile: {facts.filename}")
        print(f"Language: {facts.language}")
        print(f"Parse status: {facts.parse_status}")

        print("\nEndpoints:")

        if not facts.api_endpoints:
            print("  No API endpoints detected.")
        else:
            for endpoint in facts.api_endpoints:
                print(
                    f"  {endpoint.method} "
                    f"{endpoint.path} "
                    f"-> {endpoint.handler_name}"
                )

    print("\n" + "=" * 70)
    print("UPDATED ENGINEERING KNOWLEDGE")
    print("=" * 70)

    if result.updated_engineering_knowledge is None:
        print("No updated engineering knowledge produced.")
    else:
        print("\nREADME:")
        print(
            result.updated_engineering_knowledge
            .readme
            .content
        )

        print("\nAPI DOCUMENTATION:")
        print(
            result.updated_engineering_knowledge
            .apiDocumentation
            .content
        )

        print("\nARCHITECTURE:")
        print(
            result.updated_engineering_knowledge
            .architectureDocumentation
            .content
        )

        print("\nMERMAID DIAGRAMS:")

        diagrams = (
            result.updated_engineering_knowledge
            .architectureDocumentation
            .mermaidDiagrams
        )

        if not diagrams:
            print("  No Mermaid diagrams extracted.")
        else:
            for diagram in diagrams:
                print(f"\n--- {diagram.id} ---")
                print(diagram.content)

    print("\n" + "=" * 70)
    print("REPO LENS ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
