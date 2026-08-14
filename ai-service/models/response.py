from typing import Literal

from pydantic import BaseModel


class AnalysisMetadata(BaseModel):
    repositoryId: str
    commitHash: str
    analysisTimestamp: str
    processingTimeMs: int


class DriftAnalysis(BaseModel):
    driftDetected: bool
    affectedArtifacts: list[
        Literal["README", "ARCHITECTURE", "API_DOCUMENTATION"]
    ]
    overallReason: str
    confidence: float


class SuggestedUpdate(BaseModel):
    artifactType: Literal["README", "ARCHITECTURE", "API_DOCUMENTATION"]
    artifactPath: str
    changeType: Literal["MODIFY", "CREATE"]
    section: str | None = None
    currentContent: str
    suggestedContent: str
    explanation: str
    confidence: float


class DebugInfo(BaseModel):
    codeElementsAnalyzed: list[str]
    documentationSectionsReviewed: list[str]
    changesIdentified: list[str]


class AnalyzeResponse(BaseModel):
    analysisMetadata: AnalysisMetadata
    driftAnalysis: DriftAnalysis
    suggestedUpdates: list[SuggestedUpdate]
    noChangeReason: str | None = None
    debugInfo: DebugInfo