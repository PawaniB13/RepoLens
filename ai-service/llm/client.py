from abc import ABC, abstractmethod

from models.semantic_analysis import SemanticAnalysisResult


class LLMClient(ABC):
    """
    Provider-independent interface for LLM inference.

    The rest of the AI service depends only on this abstraction,
    allowing the underlying LLM provider or model to be replaced
    without changing the analysis pipeline.
    """

    @abstractmethod
    def analyze(
        self,
        context: dict,
    ) -> SemanticAnalysisResult:
        """
        Analyze structured repository context and return a
        validated semantic analysis result.

        Implementations are responsible for communicating with
        the configured LLM provider and converting its response
        into the internal semantic-analysis model.
        """

        raise NotImplementedError