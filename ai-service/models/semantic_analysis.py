from typing import Literal

from pydantic import BaseModel, Field


ArtifactType = Literal[
    "README",
    "ARCHITECTURE",
    "API_DOCUMENTATION",
]


class SemanticArtifactAnalysis(BaseModel):
    artifactType: ArtifactType
    driftDetected: bool
    reason: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class SemanticAnalysisResult(BaseModel):
    artifacts: list[SemanticArtifactAnalysis]