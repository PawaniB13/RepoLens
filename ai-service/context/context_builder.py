from dataclasses import asdict

from models.code_facts import CodeFacts
from models.requests import AnalyzeRequest


class ContextBuilder:
    """
    Builds structured repository context for downstream RepoLens analysis.

    This component is responsible for assembling the information required
    by later analysis stages.

    It does not:
    - perform semantic interpretation
    - detect documentation drift
    - perform LLM inference
    - generate documentation
    - perform Git operations
    """

    def build(
        self,
        request: AnalyzeRequest,
        code_facts: list[CodeFacts],
    ) -> dict:
        """
        Build deterministic analysis context from the analysis request
        and extracted code facts.
        """

        return {
            "repositoryMetadata": request.repositoryMetadata.model_dump(),
            "webhookEvent": request.webhookEvent.model_dump(),
            "gitDiff": request.gitDiff.model_dump(),
            "changedCodeFiles": [
                {
                    "filename": changed_file.filename,
                    "language": changed_file.language,
                    "content": changed_file.content,
                    "codeFacts": asdict(facts),
                }
                for changed_file, facts in zip(
                    request.changedCodeFiles.files,
                    code_facts,
                )
            ],
            "currentEngineeringKnowledge": (
                request.currentEngineeringKnowledge.model_dump()
            ),
            "previousAnalysisMetadata": (
                request.previousAnalysisMetadata.model_dump()
            ),
        }