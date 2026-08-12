from typing import Literal

from pydantic import BaseModel


class RepositoryMetadata(BaseModel):
    repositoryId: str
    repositoryName: str
    repositoryUrl: str
    description: str
    mainTechnologies: list[str]
    architectureType: str


class WebhookEvent(BaseModel):
    type: Literal["PULL_REQUEST_MERGED", "DIRECT_PUSH"]
    branchName: str
    previousCommitHash: str
    commitHash: str
    commitMessage: str
    author: str
    timestamp: str


class ChangedFile(BaseModel):
    filename: str
    status: Literal["ADDED", "MODIFIED", "DELETED"]
    linesAdded: int
    linesRemoved: int
    diffContent: str


class DiffSummary(BaseModel):
    totalFilesChanged: int
    totalLinesAdded: int
    totalLinesRemoved: int


class GitDiff(BaseModel):
    filesChanged: list[ChangedFile]
    summary: DiffSummary