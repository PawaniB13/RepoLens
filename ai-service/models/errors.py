from pydantic import BaseModel, Field


class InvalidRequestDetails(BaseModel):
    """Details describing request fields that are invalid or missing."""

    missingFields: list[str] = Field(default_factory=list)
    invalidFields: list[str] = Field(default_factory=list)


class InvalidRequestError(BaseModel):
    """Contract response for HTTP 400 invalid requests."""

    error: str
    message: str
    details: InvalidRequestDetails


class AnalysisFailedDetails(BaseModel):
    """Details describing why repository analysis failed."""

    failedFiles: list[str] = Field(default_factory=list)
    reason: str


class AnalysisFailedError(BaseModel):
    """Contract response for HTTP 422 analysis failures."""

    error: str
    message: str
    details: AnalysisFailedDetails


class InternalServerError(BaseModel):
    """Response model for unexpected internal server errors."""

    error: str
    message: str