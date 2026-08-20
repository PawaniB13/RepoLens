from models.code_facts import CodeFacts


class CodeAnalyzer:
    """
    Deterministically analyzes source code using Tree-sitter.

    The analyzer extracts structural facts from source code and returns
    them as a CodeFacts object.

    It does not perform semantic interpretation, drift detection,
    documentation analysis, or LLM inference.
    """

    SUPPORTED_LANGUAGES = {
        "python",
        "javascript",
        "java",
    }

    def analyze(
        self,
        filename: str,
        source_code: str,
        language: str,
    ) -> CodeFacts:
        """
        Analyze a source file and return its deterministic code facts.
        """

        normalized_language = language.lower().strip()

        if normalized_language not in self.SUPPORTED_LANGUAGES:
            return CodeFacts(
                filename=filename,
                language=normalized_language,
                parse_status="unsupported_language",
            )

        # Parser implementation will be added next.
        raise NotImplementedError(
            "Tree-sitter parsing is not implemented yet."
        )