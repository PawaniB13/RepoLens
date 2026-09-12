import os

from dotenv import load_dotenv

from llm.config import LLMConfig
from llm.gemini_client import GeminiClient


load_dotenv()


def test_gemini_client_returns_semantic_analysis():
    api_key = os.getenv("GEMINI_API_KEY")

    assert api_key, "GEMINI_API_KEY is not configured."

    config = LLMConfig(
        provider="gemini",
        model="gemini-3.6-flash",
        api_key=api_key,
        timeout_seconds=30,
        max_retries=2,
    )

    client = GeminiClient(config)

    context = {
        "repositoryMetadata": {
            "repositoryName": "test-repository",
            "mainTechnologies": ["Python", "FastAPI"],
        },
        "changedCodeFiles": [
            {
                "filename": "main.py",
                "language": "python",
                "content": "from fastapi import FastAPI\n\napp = FastAPI()\n",
                "codeFacts": {
                    "filename": "main.py",
                    "language": "python",
                    "imports": ["fastapi"],
                    "classes": [],
                    "functions": [],
                    "endpoints": [],
                },
            }
        ],
        "currentEngineeringKnowledge": {
            "readme": {
                "path": "README.md",
                "content": "This project is a FastAPI application.",
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
    }

    result = client.analyze(context)

    assert result.artifacts
    assert len(result.artifacts) == 3

    artifact_types = {
        artifact.artifactType
        for artifact in result.artifacts
    }

    assert artifact_types == {
        "README",
        "ARCHITECTURE",
        "API_DOCUMENTATION",
    }

    for artifact in result.artifacts:
        assert artifact.reason
        assert 0.0 <= artifact.confidence <= 1.0