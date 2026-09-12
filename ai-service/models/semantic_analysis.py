from typing import Literal

from pydantic import BaseModel


ArtifactType = Literal[
    "README",
    "ARCHITECTURE",
    "API_DOCUMENTATION",
]


class SemanticArtifactAnalysis(BaseModel):
    """
    Semantic assessment of a single supported engineering knowledge artifact.

    This model represents the LLM's interpretation of whether the artifact
    is still consistent with the current repository state.
    """

    artifactType: ArtifactType
    driftDetected: bool
    reason: str
    confidence: float


class SemanticAnalysisResult(BaseModel):
    """
    Structured semantic analysis returned by the LLM layer.

    Drift detection consumes this result and makes the deterministic
    application-level decision about the final DriftAnalysis.
    """

    artifacts: list[SemanticArtifactAnalysis]