from drift.detector import DriftDetector
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)


def test_detector_reports_no_drift_when_no_artifact_is_affected():
    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=False,
                reason="README remains consistent.",
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="Architecture remains consistent.",
                confidence=0.90,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation remains consistent.",
                confidence=0.92,
            ),
        ]
    )

    result = DriftDetector().detect(semantic_analysis)

    assert result.driftDetected is False
    assert result.affectedArtifacts == []
    assert result.confidence == 0.90


def test_detector_reports_affected_artifact():
    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README no longer reflects the current API.",
                confidence=0.94,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="Architecture remains consistent.",
                confidence=0.91,
            ),
        ]
    )

    result = DriftDetector().detect(semantic_analysis)

    assert result.driftDetected is True
    assert result.affectedArtifacts == ["README"]
    assert "README" in result.overallReason
    assert result.confidence == 0.94


def test_detector_handles_multiple_affected_artifacts_conservatively():
    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README is outdated.",
                confidence=0.94,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=True,
                reason="Architecture diagram is outdated.",
                confidence=0.81,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation remains consistent.",
                confidence=0.97,
            ),
        ]
    )

    result = DriftDetector().detect(semantic_analysis)

    assert result.driftDetected is True
    assert result.affectedArtifacts == [
        "README",
        "ARCHITECTURE",
    ]
    assert "README is outdated." in result.overallReason
    assert "Architecture diagram is outdated." in result.overallReason
    assert result.confidence == 0.81


def test_detector_handles_empty_semantic_analysis():
    semantic_analysis = SemanticAnalysisResult(
        artifacts=[]
    )

    result = DriftDetector().detect(semantic_analysis)

    assert result.driftDetected is False
    assert result.affectedArtifacts == []
    assert result.confidence == 0.0