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


class ChangedCodeFile(BaseModel):
    filename: str
    language: str
    content: str


class ChangedCodeFiles(BaseModel):
    description: str
    files: list[ChangedCodeFile]
    maxTotalBytes: int | None = None


class ReadmeKnowledge(BaseModel):
    path: str
    content: str
    lastUpdated: str | None

class MermaidDiagram(BaseModel):
    id: str | None = None
    type: str
    content: str

class ArchitectureDocumentation(BaseModel):
    path: str
    content: str
    lastUpdated: str | None
    mermaidDiagrams: list[MermaidDiagram]

class ApiDocumentation(BaseModel):
    path: str
    content: str
    lastUpdated: str | None


class CurrentEngineeringKnowledge(BaseModel):
    readme: ReadmeKnowledge
    architectureDocumentation: ArchitectureDocumentation
    apiDocumentation: ApiDocumentation


class PreviousAnalysisMetadata(BaseModel):
    previousCommitHash: str | None
    previousAnalysisTimestamp: str | None
    previousDriftDetected: bool | None
    previousEngineeringTruthScore: float | None


class AnalyzeRequest(BaseModel):
    repositoryMetadata: RepositoryMetadata
    webhookEvent: WebhookEvent
    gitDiff: GitDiff
    changedCodeFiles: ChangedCodeFiles
    currentEngineeringKnowledge: CurrentEngineeringKnowledge
    previousAnalysisMetadata: PreviousAnalysisMetadata