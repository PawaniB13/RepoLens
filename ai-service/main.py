from fastapi import FastAPI

from models.requests import AnalyzeRequest


app = FastAPI(title="RepoLens AI Service")


@app.get("/")
def root():
    return {"message": "RepoLens AI Service is running!"}


@app.post("/api/v1/analyze")
def analyze(request: AnalyzeRequest):
    return {
        "message": "Analysis request received successfully",
        "repositoryId": request.repositoryMetadata.repositoryId,
        "commitHash": request.webhookEvent.commitHash
    }