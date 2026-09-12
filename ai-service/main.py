import time
from datetime import datetime, timezone
from functools import lru_cache

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from application.pipeline_factory import create_analysis_pipeline
from exceptions import AnalysisFailedException
from models.errors import (
    AnalysisFailedError,
    InternalServerError,
)
from models.requests import AnalyzeRequest
from models.response import AnalyzeResponse
from pipeline.analyzer import AnalysisPipeline


app = FastAPI(title="RepoLens AI Service")


@lru_cache
def get_analysis_pipeline() -> AnalysisPipeline:
    """
    Create and cache the configured analysis pipeline.

    The pipeline is initialized lazily when the analyze endpoint
    first requires it, rather than when the application module
    is imported.
    """

    return create_analysis_pipeline()


@app.exception_handler(AnalysisFailedException)
def handle_analysis_failed(
    request: Request,
    exc: AnalysisFailedException,
):
    """
    Convert analysis-processing failures into the contract-defined
    HTTP 422 response.
    """

    error_response = AnalysisFailedError(
        error="ANALYSIS_FAILED",
        message=exc.message,
        details={
            "failedFiles": exc.failed_files,
            "reason": exc.reason,
        },
    )

    return JSONResponse(
        status_code=422,
        content=error_response.model_dump(),
    )


@app.exception_handler(Exception)
def handle_internal_server_error(
    request: Request,
    exc: Exception,
):
    """
    Convert unexpected internal failures into a safe HTTP 500 response.

    Internal exception details are intentionally not exposed to the
    API caller.
    """

    error_response = InternalServerError(
        error="INTERNAL_ERROR",
        message="An unexpected internal error occurred.",
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(),
    )


@app.get("/")
def root():
    return {"message": "RepoLens AI Service is running!"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(
    request: AnalyzeRequest,
    pipeline: AnalysisPipeline = Depends(get_analysis_pipeline),
):
    start_time = time.perf_counter()

    result = pipeline.analyze(request)

    processing_time_ms = int(
        (time.perf_counter() - start_time) * 1000
    )

    return AnalyzeResponse(
        analysisMetadata={
            "repositoryId": request.repositoryMetadata.repositoryId,
            "commitHash": request.webhookEvent.commitHash,
            "analysisTimestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "processingTimeMs": processing_time_ms,
        },
        driftAnalysis=result.drift_analysis,
        suggestedUpdates=result.suggested_updates,
        noChangeReason=(
            None
            if result.drift_analysis.driftDetected
            else result.drift_analysis.overallReason
        ),
        debugInfo={
            "codeElementsAnalyzed": [
                element
                for facts in result.code_facts
                for element in (
                    [f"class:{item.name}" for item in facts.classes]
                    + [
                        f"method:{item.class_name}.{item.method_name}"
                        for item in facts.methods
                    ]
                    + [
                        f"function:{item.name}"
                        for item in facts.functions
                    ]
                    + [
                        f"endpoint:{item.method} {item.path}"
                        for item in facts.api_endpoints
                    ]
                )
            ],
            "documentationSectionsReviewed": [],
            "changesIdentified": [
                (
                    f"{changed_file.status}: "
                    f"{changed_file.filename} "
                    f"(+{changed_file.linesAdded}/"
                    f"-{changed_file.linesRemoved})"
                )
                for changed_file in request.gitDiff.filesChanged
            ],
        },
    )
