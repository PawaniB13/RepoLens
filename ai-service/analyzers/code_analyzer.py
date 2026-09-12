from analyzers.python_analyzer import PythonAnalyzer
from models.code_facts import CodeFacts


class CodeAnalyzer:
    """
    Orchestrates deterministic source-code analysis.

    This class selects the appropriate language-specific analyzer
    and returns deterministic CodeFacts.

    It does not perform semantic interpretation, drift detection,
    documentation analysis, or LLM inference.
    """

    _ANALYZERS = {
        "python": PythonAnalyzer,
    }

    def analyze(
        self,
        filename: str,
        source_code: str,
        language: str,
    ) -> CodeFacts:
        """
        Analyze a source file using the registered language analyzer.

        Unsupported or currently unimplemented languages are returned
        as unsupported_language rather than raising an exception.
        """

        normalized_language = language.lower().strip()

        analyzer_class = self._ANALYZERS.get(normalized_language)

        if analyzer_class is None:
            return CodeFacts(
                filename=filename,
                language=normalized_language,
                parse_status="unsupported_language",
            )

        analyzer = analyzer_class()

        return analyzer.analyze(
            filename=filename,
            source_code=source_code,
        )