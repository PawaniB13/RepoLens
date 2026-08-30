from dataclasses import dataclass, field
from typing import Literal


# ==================== HELPER MODELS ====================

@dataclass
class CodeClass:
    """Represents a class/interface/type definition."""
    name: str
    line_start: int
    line_end: int


@dataclass
class CodeMethod:
    """Represents a method within a class."""
    class_name: str
    method_name: str
    line_start: int
    line_end: int


@dataclass
class CodeFunction:
    """Represents a standalone function."""
    name: str
    line_start: int
    line_end: int


@dataclass
class CodeImport:
    """Represents an import statement."""
    statement: str
    package: str
    line: int


@dataclass
class CodeEndpoint:
    """Represents an HTTP API endpoint."""
    method: str
    path: str
    handler_name: str
    line_start: int
    line_end: int


# ==================== MAIN MODEL ====================

@dataclass
class CodeFacts:
    """
    A minimal, deterministically-extracted representation of a source file.

    Extracted by Tree-sitter without semantic interpretation.
    Designed to support drift detection for README, architecture,
    and API documentation.

    Responsibility:
        "What structural facts can we extract from this file?"

    NOT:
        "Did this file change?" (Git's responsibility)
        "What does this code mean?" (LLM's responsibility)
    """

    # Identity
    filename: str
    language: str

    # Structural information
    classes: list[CodeClass] = field(default_factory=list)
    methods: list[CodeMethod] = field(default_factory=list)
    functions: list[CodeFunction] = field(default_factory=list)

    # Dependencies
    imports: list[CodeImport] = field(default_factory=list)

    # API exposure
    api_endpoints: list[CodeEndpoint] = field(default_factory=list)

    # Parse status
    parse_status: Literal[
        "unknown",
        "success",
        "unsupported_language",
        "parse_error",
    ] = "unknown"

    parse_error: str | None = None

    # Optional context
    line_count: int | None = None
    file_size_bytes: int | None = None

    def is_successfully_parsed(self) -> bool:
        """Return True if the file was parsed successfully."""
        return self.parse_status == "success"