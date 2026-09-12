from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """
    Provider-independent configuration for LLM inference.

    This model contains configuration required by an LLM client
    without coupling the AI service to a specific LLM provider.
    """

    provider: str = Field(
        min_length=1,
        description="Identifier of the configured LLM provider.",
    )

    model: str = Field(
        min_length=1,
        description="Identifier of the model used for inference.",
    )

    api_key: str = Field(
        min_length=1,
        description="Credential used by the configured LLM provider.",
    )

    base_url: str | None = Field(
        default=None,
        description="Optional provider endpoint override.",
    )

    timeout_seconds: float = Field(
        default=30.0,
        gt=0,
        description="Maximum time allowed for a single LLM request.",
    )

    max_retries: int = Field(
        default=2,
        ge=0,
        description="Maximum number of retries for a failed LLM request.",
    )