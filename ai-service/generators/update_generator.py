from abc import ABC, abstractmethod

from models.response import SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult


class UpdateGenerator(ABC):
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
    def generate(
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