import json

from google import genai
from google.genai import types
from pydantic import TypeAdapter

from generators.llm_update_generator import UpdateGenerationClient
from llm.config import LLMConfig
from models.response import SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult


class GeminiUpdateClient(UpdateGenerationClient):
    """
    Gemini-backed implementation of UpdateGenerationClient.

    This client is responsible only for generating structured
    engineering-knowledge update suggestions.

    It does not:
    - detect drift
    - analyze source code
    - perform Git operations
    - communicate with GitHub
    - persist results
    """

    def __init__(self, config: LLMConfig) -> None:
        self.config = config

        self.client = genai.Client(
            api_key=config.api_key,
            http_options=types.HttpOptions(
                timeout=int(config.timeout_seconds * 1000),
            ),
        )

        self._updates_adapter = TypeAdapter(
            list[SuggestedUpdate]
        )

    def generate_updates(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        """
        Generate complete, contract-valid update suggestions
        for artifacts identified as drifted.
        """

        prompt = self._build_prompt(
            context=context,
            semantic_analysis=semantic_analysis,
        )

        interaction = self.client.interactions.create(
            model=self.config.model,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": self._updates_adapter.json_schema(),
            },
        )

        if not interaction.output_text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        return self._parse_updates(
            interaction.output_text,
        )

    def _parse_updates(
        self,
        output_text: str,
    ) -> list[SuggestedUpdate]:
        """
        Parse and validate Gemini's structured update response.
        """

        try:
            payload = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned invalid JSON for update generation."
            ) from exc

        return self._updates_adapter.validate_python(payload)

    def _build_prompt(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> str:
        """
        Build the update-generation prompt from repository context
        and validated semantic analysis.
        """

        affected_artifacts = [
            artifact.artifactType
            for artifact in semantic_analysis.artifacts
            if artifact.driftDetected
        ]

        return f"""
You are the engineering-knowledge update generation component
of RepoLens.

Your task is to generate complete documentation update suggestions
for the engineering-knowledge artifacts that semantic analysis has
identified as drifted.

Supported artifacts:
- README
- ARCHITECTURE
- API_DOCUMENTATION

Only generate updates for these affected artifacts:

{json.dumps(affected_artifacts, indent=2)}

Rules:

1. Use only facts present in the provided repository context.
2. Do not invent repository behavior, APIs, technologies, classes,
   relationships, or architecture.
3. Preserve information that remains correct.
4. Each suggestion must describe a complete update to the relevant
   documentation section or artifact.
5. Do not return partial fragments.
6. Include the existing relevant content in currentContent.
7. Include the complete replacement content in suggestedContent.
8. Explain why the update is required.
9. Confidence must be between 0 and 1.
10. Use the exact supported artifact type names.
11. For ARCHITECTURE updates, suggestedContent must contain the
    complete Mermaid diagram when a diagram is being updated.
12. Do not generate suggestions for artifacts that were not identified
    as drifted.
13. If the available evidence is insufficient to produce a trustworthy
    update, do not invent content.
14. Return a JSON array matching the required SuggestedUpdate schema.
15. Do not return markdown fences or explanatory text outside the
    JSON array.

Semantic analysis:

{semantic_analysis.model_dump_json(indent=2)}

Repository context:

{json.dumps(context, indent=2, default=str)}
""".strip()