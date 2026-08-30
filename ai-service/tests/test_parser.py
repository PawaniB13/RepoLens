import pytest

from analyzers.parser import ParserFactory


@pytest.mark.parametrize(
    "language",
    ["python", "javascript", "java"],
)
def test_create_supported_parser(language):
    parser = ParserFactory.create(language)

    assert parser is not None


def test_create_parser_is_case_insensitive():
    parser = ParserFactory.create("Python")

    assert parser is not None


def test_create_parser_rejects_unsupported_language():
    with pytest.raises(ValueError, match="Unsupported programming language"):
        ParserFactory.create("ruby")