from google import genai
from google.genai import types

from llm.client import LLMClient
from llm.config import LLMConfig
from models.semantic_analysis import SemanticAnalysisResult


class GeminiClient(LLMClient):
    """
    Gemini-backed implementation of the provider-independent LLMClient.

    This class is responsible for:
    - communicating with the Gemini API
    - sending structured repository-analysis context
    - requesting structured JSON output
    - validating the response against SemanticAnalysisResult

    It does not:
    - detect drift itself
    - inspect source code directly
    - generate final documentation
    - perform Git operations
    """

    def __init__(self, config: LLMConfig):
        self.config = config

        self.client = genai.Client(
            api_key=config.api_key,
            http_options=types.HttpOptions(
                timeout=int(config.timeout_seconds * 1000),
            ),
        )

    def analyze(
        self,
        context: dict,
    ) -> SemanticAnalysisResult:
        """
        Analyze repository context using Gemini and return
        a validated semantic-analysis result.
        """

        prompt = self._build_prompt(context)

        interaction = self.client.interactions.create(
            model=self.config.model,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": SemanticAnalysisResult.model_json_schema(),
            },
        )

        if not interaction.output_text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        return SemanticAnalysisResult.model_validate_json(
            interaction.output_text
        )

    def _build_prompt(self, context: dict) -> str:
        """
        Build the semantic-analysis prompt from structured
        deterministic repository context.
        """

        return f"""
You are the semantic analysis component of RepoLens.

Your task is to determine whether the current repository state
is inconsistent with any supported engineering knowledge artifact.

Supported artifacts:
- README
- ARCHITECTURE
- API_DOCUMENTATION

Important rules:

1. Use only the repository context provided below.
2. Do not invent repository facts.
3. Deterministic code facts are authoritative.
4. Analyze semantic meaning rather than merely detecting that files changed.
5. Mark an artifact as drifted only when its documented knowledge
   is inconsistent with the current repository state.
6. If there is insufficient evidence to establish drift, do not
   claim drift.
7. Provide a concise reason for every artifact.
8. Confidence must represent your confidence in the decision.
9. Analyze all three supported artifacts independently.

Repository analysis context:

{context}
""".strip()