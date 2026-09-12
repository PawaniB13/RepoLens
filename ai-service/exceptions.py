class AnalysisFailedException(Exception):
    """
    Raised when a valid analysis request cannot be processed.

    This exception represents an analysis-processing failure,
    not a malformed HTTP request.
    """

    def __init__(
        self,
        message: str,
        failed_files: list[str] | None = None,
        reason: str = "",
    ) -> None:
        super().__init__(message)

        self.message = message
        self.failed_files = failed_files or []
        self.reason = reason