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
from pipeline.result_validator import AnalysisResultValidator


@dataclass
class PipelineAnalysisResult:
    code_facts: list[CodeFacts]
    semantic_analysis: SemanticAnalysisResult
    drift_analysis: DriftAnalysis
    suggested_updates: list[SuggestedUpdate]


class AnalysisPipeline:
    def __init__(
        self,
        llm_client: LLMClient,
        update_generator: LLMUpdateGenerator,
        code_analyzer: CodeAnalyzer | None = None,
        context_builder: ContextBuilder | None = None,
        drift_detector: DriftDetector | None = None,
        result_validator: AnalysisResultValidator | None = None,
    ) -> None:
        self._code_analyzer = code_analyzer or CodeAnalyzer()
        self._context_builder = context_builder or ContextBuilder()
        self._llm_client = llm_client
        self._drift_detector = drift_detector or DriftDetector()
        self._update_generator = update_generator
        self._result_validator = (
            result_validator or AnalysisResultValidator()
        )

    def analyze(self, request: AnalyzeRequest) -> PipelineAnalysisResult:
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
        return [
            self._code_analyzer.analyze(
                filename=changed_file.filename,
                source_code=changed_file.content,
                language=changed_file.language,
            )
            for changed_file in request.changedCodeFiles.files
        ]