from dataclasses import dataclass

from analyzers.code_analyzer import CodeAnalyzer
from context.context_builder import ContextBuilder
from drift.detector import DriftDetector
from generators.llm_update_generator import LLMUpdateGenerator
from llm.client import LLMClient
from models.code_facts import CodeFacts
from models.requests import AnalyzeRequest
from models.response import DriftAnalysis, SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult


@dataclass
class PipelineAnalysisResult:
    """
    Internal result produced by the analysis pipeline.

    This is not the public FastAPI response model.
    It contains the intermediate results required by later
    pipeline stages and response construction.
    """

    code_facts: list[CodeFacts]
    semantic_analysis: SemanticAnalysisResult
    drift_analysis: DriftAnalysis
    suggested_updates: list[SuggestedUpdate]


class AnalysisPipeline:
    """
    Orchestrates the RepoLens analysis flow.

    The pipeline coordinates:
        1. deterministic code analysis
        2. structured context construction
        3. semantic LLM analysis
        4. engineering-knowledge drift detection
        5. engineering-knowledge update generation

    It does not:
        - perform Git operations
        - communicate with GitHub
        - implement language-specific parsing
        - implement LLM-provider logic
        - generate documentation directly
        - persist analysis results
    """

    def __init__(
        self,
        llm_client: LLMClient,
        update_generator: LLMUpdateGenerator,
        code_analyzer: CodeAnalyzer | None = None,
        context_builder: ContextBuilder | None = None,
        drift_detector: DriftDetector | None = None,
    ) -> None:
        """
        Initialize the analysis pipeline.

        The LLM client and update generator are injected so the
        pipeline remains independent of specific providers or models.
        """

        self._code_analyzer = code_analyzer or CodeAnalyzer()
        self._context_builder = context_builder or ContextBuilder()
        self._llm_client = llm_client
        self._drift_detector = drift_detector or DriftDetector()
        self._update_generator = update_generator

    def analyze(
        self,
        request: AnalyzeRequest,
    ) -> PipelineAnalysisResult:
        """
        Execute the deterministic and semantic analysis pipeline.
        """

        code_facts = self._analyze_changed_files(request)

        context = self._context_builder.build(
            request=request,
            code_facts=code_facts,
        )

        semantic_analysis = self._llm_client.analyze(
            context=context,
        )

        drift_analysis = self._drift_detector.detect(
            semantic_analysis=semantic_analysis,
        )

        suggested_updates = self._update_generator.generate(
            context=context,
            semantic_analysis=semantic_analysis,
        )

        return PipelineAnalysisResult(
            code_facts=code_facts,
            semantic_analysis=semantic_analysis,
            drift_analysis=drift_analysis,
            suggested_updates=suggested_updates,
        )

    def _analyze_changed_files(
        self,
        request: AnalyzeRequest,
    ) -> list[CodeFacts]:
        """
        Deterministically analyze every changed source file.

        The returned list preserves the exact ordering of
        request.changedCodeFiles.files so that each CodeFacts
        object corresponds to the source file at the same index.
        """

        return [
            self._code_analyzer.analyze(
                filename=changed_file.filename,
                source_code=changed_file.content,
                language=changed_file.language,
            )
            for changed_file in request.changedCodeFiles.files
        ]