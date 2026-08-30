import pytest

from analyzers.code_analyzer import CodeAnalyzer


def test_unsupported_language():
    analyzer = CodeAnalyzer()

    facts = analyzer.analyze(
        filename="example.xyz",
        source_code="some code",
        language="xyz",
    )

    assert facts.parse_status == "unsupported_language"
    assert facts.filename == "example.xyz"
    assert facts.language == "xyz"