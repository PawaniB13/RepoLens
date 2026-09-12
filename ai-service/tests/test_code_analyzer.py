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

def test_python_analysis_delegates_to_python_analyzer():
    analyzer = CodeAnalyzer()

    facts = analyzer.analyze(
        filename="main.py",
        source_code="""
def hello():
    return "hello"
""",
        language="python",
    )

    assert facts.filename == "main.py"
    assert facts.language == "python"
    assert facts.parse_status == "success"
    assert len(facts.functions) == 1
    assert facts.functions[0].name == "hello"