from tree_sitter import Language, Parser

import tree_sitter_java
import tree_sitter_javascript
import tree_sitter_python


class ParserFactory:
    """
    Creates Tree-sitter parsers for supported programming languages.

    Responsibility:
        Select and configure the appropriate Tree-sitter grammar.

    This class does not analyze syntax trees or extract code facts.
    """

    _LANGUAGE_BUILDERS = {
        "python": lambda: Language(tree_sitter_python.language()),
        "javascript": lambda: Language(tree_sitter_javascript.language()),
        "java": lambda: Language(tree_sitter_java.language()),
    }

    @classmethod
    def create(cls, language: str) -> Parser:
        """
        Create a Tree-sitter parser for the requested language.

        Raises:
            ValueError: If the language is not supported.
        """
        normalized_language = language.lower().strip()

        builder = cls._LANGUAGE_BUILDERS.get(normalized_language)

        if builder is None:
            raise ValueError(
                f"Unsupported programming language: {language}"
            )

        parser = Parser()
        parser.language = builder()

        return parser