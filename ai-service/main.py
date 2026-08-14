from fastapi import FastAPI

from models.requests import AnalyzeRequest
from models.response import AnalyzeResponse


app = FastAPI(title="RepoLens AI Service")


@app.get("/")
def root():
    return {"message": "RepoLens AI Service is running!"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    return {
        "analysisMetadata": {
            "repositoryId": request.repositoryMetadata.repositoryId,
            "commitHash": request.webhookEvent.commitHash,
            "analysisTimestamp": "2026-08-13T13:00:00Z",
            "processingTimeMs": 100
        },
        "driftAnalysis": {
            "driftDetected": True,
            "affectedArtifacts": [
                "README",
                "ARCHITECTURE",
                "API_DOCUMENTATION"
            ],
            "overallReason": "Test response: authentication documentation is outdated.",
            "confidence": 0.95
        },
        "suggestedUpdates": [
            {
                "artifactType": "README",
                "artifactPath": "README.md",
                "changeType": "MODIFY",
                "section": "Authentication",
                "currentContent": "The application uses JWT authentication.",
                "suggestedContent": "The application uses OAuth2 authentication.",
                "explanation": "Test suggestion for validating the response contract.",
                "confidence": 0.95
            }
        ],
        "noChangeReason": None,
        "debugInfo": {
            "codeElementsAnalyzed": [
                "AuthService"
            ],
            "documentationSectionsReviewed": [
                "README - Authentication"
            ],
            "changesIdentified": [
                "Authentication mechanism changed"
            ]
        }
    }