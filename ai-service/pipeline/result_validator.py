from models.response import SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult


class AnalysisResultValidator:
    """
    Validates consistency between semantic drift analysis and
    generated engineering-knowledge updates.

    This validator enforces RepoLens contract-level invariants.

    It does not:
    - perform LLM inference
    - detect drift
    - generate updates
    - modify documents
    - perform Git operations
    """

    def validate(
        self,
        semantic_analysis: SemanticAnalysisResult,
        suggested_updates: list[SuggestedUpdate],
    ) -> None:
        """
        Validate the relationship between drift decisions and updates.

        Raises:
            ValueError: If the analysis result violates contract rules.
        """

        drifted_artifacts = {
            artifact.artifactType
            for artifact in semantic_analysis.artifacts
            if artifact.driftDetected
        }

        update_artifacts = {
            update.artifactType
            for update in suggested_updates
        }

        if not drifted_artifacts and suggested_updates:
            raise ValueError(
                "Suggested updates must be empty when no drift is detected."
            )

        missing_updates = (
            drifted_artifacts - update_artifacts
        )

        if missing_updates:
            missing = ", ".join(
                sorted(missing_updates)
            )

            raise ValueError(
                "Every drifted artifact must have at least one "
                f"suggested update. Missing updates for: {missing}."
            )

        unexpected_updates = (
            update_artifacts - drifted_artifacts
        )

        if unexpected_updates:
            unexpected = ", ".join(
                sorted(unexpected_updates)
            )

            raise ValueError(
                "Suggested updates must only target drifted "
                f"artifacts. Unexpected updates for: {unexpected}."
            )