from models.response import DriftAnalysis
from models.semantic_analysis import SemanticAnalysisResult


class DriftDetector:
    """
    Converts semantic artifact analysis into the contract-level
    DriftAnalysis result.

    This component does not:
    - perform LLM inference
    - inspect source code directly
    - generate documentation
    - perform Git operations

    It only interprets the structured semantic analysis result and
    produces the final drift decision.
    """

    def detect(
        self,
        semantic_analysis: SemanticAnalysisResult,
    ) -> DriftAnalysis:
        """
        Determine whether engineering knowledge has drifted.

        Drift exists when at least one supported artifact has been
        identified by the semantic analysis as inconsistent with
        the current repository state.
        """

        affected_artifacts = [
            artifact.artifactType
            for artifact in semantic_analysis.artifacts
            if artifact.driftDetected
        ]

        drift_detected = bool(affected_artifacts)

        if drift_detected:
            affected_results = [
                artifact
                for artifact in semantic_analysis.artifacts
                if artifact.driftDetected
            ]

            overall_reason = " ".join(
                artifact.reason.strip()
                for artifact in affected_results
                if artifact.reason.strip()
            )

            if not overall_reason:
                overall_reason = (
                    "One or more supported engineering knowledge "
                    "artifacts were identified as inconsistent with "
                    "the current repository state."
                )

            confidence = min(
                artifact.confidence
                for artifact in affected_results
            )

        else:
            overall_reason = (
                "No supported engineering knowledge artifact "
                "was identified as inconsistent with the current "
                "repository state."
            )

            if semantic_analysis.artifacts:
                confidence = min(
                    artifact.confidence
                    for artifact in semantic_analysis.artifacts
                )
            else:
                confidence = 0.0

        return DriftAnalysis(
            driftDetected=drift_detected,
            affectedArtifacts=affected_artifacts,
            overallReason=overall_reason,
            confidence=confidence,
        )