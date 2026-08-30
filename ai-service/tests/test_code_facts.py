from models.code_facts import CodeFacts


def test_code_facts_defaults():
    facts = CodeFacts(
        filename="src/auth.py",
        language="python",
    )

    assert facts.filename == "src/auth.py"
    assert facts.language == "python"

    assert facts.classes == []
    assert facts.methods == []
    assert facts.functions == []
    assert facts.imports == []
    assert facts.api_endpoints == []

    assert facts.parse_status == "unknown"
    assert facts.parse_error is None

    assert facts.line_count is None
    assert facts.file_size_bytes is None

    assert facts.is_successfully_parsed() is False

def test_code_facts_successful_parse():
    facts = CodeFacts(
        filename="src/auth.py",
        language="python",
        parse_status="success",
        line_count=42,
        file_size_bytes=1200,
    )

    assert facts.is_successfully_parsed() is True
    assert facts.line_count == 42
    assert facts.file_size_bytes == 1200