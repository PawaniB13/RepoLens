from dataclasses import dataclass

from analyzers.code_analyzer import CodeAnalyzer
from context.context_builder import ContextBuilder
from drift.detector import DriftDetector
from generators.document_update_service import DocumentUpdateService
from generators.engineering_knowledge_update_service import (
    EngineeringKnowledgeUpdateService,
)
from generators.llm_update_generator import LLMUpdateGenerator
from generators.mermaid_extractor import MermaidExtractor
from llm.client import LLMClient
from models.code_facts import CodeFacts
from models.requests import AnalyzeRequest, CurrentEngineeringKnowledge
from models.response import DriftAnalysis, SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult
from pipeline.result_validator import AnalysisResultValidator


@dataclass
class PipelineAnalysisResult:
    """
    Internal result produced by the analysis pipeline.

    This is not the public FastAPI response model.
    It contains the intermediate and final internal results
    required by later pipeline stages and response construction.
    """

    code_facts: list[CodeFacts]
    semantic_analysis: SemanticAnalysisResult
    drift_analysis: DriftAnalysis
    suggested_updates: list[SuggestedUpdate]
    updated_engineering_knowledge: CurrentEngineeringKnowledge | None = None

class AnalysisPipeline:
    """
    Orchestrates the RepoLens analysis flow.

    The pipeline coordinates:
        1. deterministic code analysis
        2. structured context construction
        3. semantic LLM analysis
        4. engineering-knowledge drift detection
        5. engineering-knowledge update generation
        6. contract-level result validation
        7. deterministic application of generated updates

    It does not:
        - perform Git operations
        - communicate with GitHub
        - implement language-specific parsing
        - implement LLM-provider logic
        - persist analysis results
    """

    def __init__(
        self,
        llm_client: LLMClient,
        update_generator: LLMUpdateGenerator,
        code_analyzer: CodeAnalyzer | None = None,
        context_builder: ContextBuilder | None = None,
        drift_detector: DriftDetector | None = None,
        result_validator: AnalysisResultValidator | None = None,
        knowledge_update_service: (
            EngineeringKnowledgeUpdateService | None
        ) = None,
    ) -> None:
        """
        Initialize the analysis pipeline.

        Dependencies are injected so the pipeline remains independent
        of specific implementations and providers.
        """

        self._code_analyzer = code_analyzer or CodeAnalyzer()
        self._context_builder = context_builder or ContextBuilder()
        self._llm_client = llm_client
        self._drift_detector = drift_detector or DriftDetector()
        self._update_generator = update_generator
        self._result_validator = (
            result_validator or AnalysisResultValidator()
        )
        self._knowledge_update_service = (
            knowledge_update_service
            or EngineeringKnowledgeUpdateService(
                document_update_service=DocumentUpdateService(),
                mermaid_extractor=MermaidExtractor(),
            )
        )

    def analyze(
        self,
        request: AnalyzeRequest,
    ) -> PipelineAnalysisResult:
        """
        Execute the complete RepoLens analysis pipeline.

        Generated updates are validated before they are applied.
        The original engineering knowledge contained in the request
        is never modified in place.
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

        self._result_validator.validate(
            semantic_analysis=semantic_analysis,
            suggested_updates=suggested_updates,
        )

        updated_engineering_knowledge = (
            self._knowledge_update_service.apply_updates(
                knowledge=request.currentEngineeringKnowledge,
                updates=suggested_updates,
            )
        )

        return PipelineAnalysisResult(
            code_facts=code_facts,
            semantic_analysis=semantic_analysis,
            drift_analysis=drift_analysis,
            suggested_updates=suggested_updates,
            updated_engineering_knowledge=updated_engineering_knowledge,
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