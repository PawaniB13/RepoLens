import pytest

from models.response import SuggestedUpdate
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)
from pipeline.result_validator import AnalysisResultValidator


def create_analysis(
    readme_drift: bool = False,
    architecture_drift: bool = False,
) -> SemanticAnalysisResult:
    return SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=readme_drift,
                reason="README analysis.",
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=architecture_drift,
                reason="Architecture analysis.",
                confidence=0.90,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation is accurate.",
                confidence=0.92,
            ),
        ]
    )


def create_update(
    artifact_type: str,
) -> SuggestedUpdate:
    return SuggestedUpdate(
        artifactType=artifact_type,
        artifactPath="README.md",
        changeType="MODIFY",
        section="Overview",
        currentContent="Old content",
        suggestedContent="New content",
        explanation="Documentation is outdated.",
        confidence=0.95,
    )


def test_accepts_no_drift_with_no_updates():
    validator = AnalysisResultValidator()

    validator.validate(
        semantic_analysis=create_analysis(),
        suggested_updates=[],
    )


def test_accepts_drift_with_matching_update():
    validator = AnalysisResultValidator()

    validator.validate(
        semantic_analysis=create_analysis(
            readme_drift=True,
        ),
        suggested_updates=[
            create_update("README"),
        ],
    )


def test_rejects_drift_without_update():
    validator = AnalysisResultValidator()

    with pytest.raises(
        ValueError,
        match="Every drifted artifact must have",
    ):
        validator.validate(
            semantic_analysis=create_analysis(
                readme_drift=True,
            ),
            suggested_updates=[],
        )


def test_rejects_updates_when_no_drift_exists():
    validator = AnalysisResultValidator()

    with pytest.raises(
        ValueError,
        match="must be empty when no drift",
    ):
        validator.validate(
            semantic_analysis=create_analysis(),
            suggested_updates=[
                create_update("README"),
            ],
        )


def test_rejects_update_for_non_drifted_artifact():
    validator = AnalysisResultValidator()

    with pytest.raises(
        ValueError,
        match="must only target drifted artifacts",
    ):
        validator.validate(
            semantic_analysis=create_analysis(
                readme_drift=True,
            ),
            suggested_updates=[
                create_update("README"),
                create_update("ARCHITECTURE"),
            ],
        )


def test_requires_updates_for_all_drifted_artifacts():
    validator = AnalysisResultValidator()

    with pytest.raises(
        ValueError,
        match="ARCHITECTURE",
    ):
        validator.validate(
            semantic_analysis=create_analysis(
                readme_drift=True,
                architecture_drift=True,
            ),
            suggested_updates=[
                create_update("README"),
            ],
        )