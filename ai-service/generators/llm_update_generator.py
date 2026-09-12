from abc import ABC, abstractmethod

from models.response import SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult


class UpdateGenerationClient(ABC):
    """
    Provider-independent interface for generating complete
    engineering-knowledge updates.

    Generators operate only after semantic analysis has identified
    affected engineering-knowledge artifacts.

    They do not:
    - perform drift detection
    - perform Git operations
    - communicate with GitHub
    - persist data
    """

    @abstractmethod
    def generate_updates(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        """
        Generate complete, contract-valid suggested updates
        for affected artifacts.

        Implementations must return complete artifact-level
        suggestions, not partial fragments.
        """

        raise NotImplementedError


class LLMUpdateGenerator:
    """
    Generates engineering-knowledge update suggestions using an
    injected provider-independent generation client.

    This component does not:
    - perform drift detection
    - analyze source code
    - perform Git operations
    - communicate with GitHub
    - persist analysis results

    It only coordinates update generation after semantic analysis.
    """

    def __init__(
        self,
        generation_client: UpdateGenerationClient,
    ) -> None:
        self._generation_client = generation_client

    def generate(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        """
        Generate suggested updates for artifacts identified as drifted.

        If semantic analysis reports no drift, no update generation
        request is made and an empty list is returned.
        """

        affected_artifacts = {
            artifact.artifactType
            for artifact in semantic_analysis.artifacts
            if artifact.driftDetected
        }

        if not affected_artifacts:
            return []

        updates = self._generation_client.generate_updates(
            context=context,
            semantic_analysis=semantic_analysis,
        )

        return [
            update
            for update in updates
            if update.artifactType in affected_artifacts
        ]