import os

from dotenv import load_dotenv

from generators.llm_update_generator import LLMUpdateGenerator
from llm.config import LLMConfig
from llm.gemini_client import GeminiClient
from llm.gemini_update_client import GeminiUpdateClient
from llm.local_semantic_client import LocalSemanticClient
from generators.local_update_client import LocalUpdateClient
from pipeline.analyzer import AnalysisPipeline


load_dotenv()


def create_analysis_pipeline() -> AnalysisPipeline:
    """
    Create the configured RepoLens analysis pipeline.

    The provider is selected using the LLM_PROVIDER environment variable.

    Supported providers:
    - gemini: real Gemini semantic analysis and update generation
    - local: deterministic quota-free local implementation

    Provider-specific clients remain behind the pipeline's abstractions.
    """

    provider = os.getenv(
        "LLM_PROVIDER",
        "gemini",
    ).strip().lower()

    if provider == "local":
        semantic_client = LocalSemanticClient()

        update_client = LocalUpdateClient()

        update_generator = LLMUpdateGenerator(
            generation_client=update_client,
        )

        return AnalysisPipeline(
            llm_client=semantic_client,
            update_generator=update_generator,
        )

    if provider != "gemini":
        raise RuntimeError(
            f"Unsupported LLM_PROVIDER: {provider}"
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    config = LLMConfig(
        provider="gemini",
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        ),
        api_key=api_key,
        timeout_seconds=float(
            os.getenv(
                "LLM_TIMEOUT_SECONDS",
                "30",
            )
        ),
        max_retries=int(
            os.getenv(
                "LLM_MAX_RETRIES",
                "2",
            )
        ),
    )

    semantic_client = GeminiClient(config)

    update_client = GeminiUpdateClient(config)

    update_generator = LLMUpdateGenerator(
        generation_client=update_client,
    )

    return AnalysisPipeline(
        llm_client=semantic_client,
        update_generator=update_generator,
    )