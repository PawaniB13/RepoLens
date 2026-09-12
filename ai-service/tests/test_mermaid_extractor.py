from generators.mermaid_extractor import MermaidExtractor


def test_extracts_single_mermaid_diagram():
    content = (
        "# Architecture\n\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    A[Client] --> B[Backend]\n"
        "    B --> C[AI Service]\n"
        "```"
    )

    extractor = MermaidExtractor()

    diagrams = extractor.extract(content)

    assert len(diagrams) == 1
    assert diagrams[0].id == "diagram-1"
    assert diagrams[0].type == "mermaid"
    assert diagrams[0].content == (
        "flowchart TD\n"
        "    A[Client] --> B[Backend]\n"
        "    B --> C[AI Service]"
    )


def test_extracts_multiple_mermaid_diagrams():
    content = (
        "# Architecture\n\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    A --> B\n"
        "```\n\n"
        "Some documentation.\n\n"
        "```mermaid\n"
        "sequenceDiagram\n"
        "    Client->>Server: Request\n"
        "    Server-->>Client: Response\n"
        "```"
    )

    extractor = MermaidExtractor()

    diagrams = extractor.extract(content)

    assert len(diagrams) == 2

    assert diagrams[0].id == "diagram-1"
    assert diagrams[0].content == (
        "flowchart TD\n"
        "    A --> B"
    )

    assert diagrams[1].id == "diagram-2"
    assert diagrams[1].content == (
        "sequenceDiagram\n"
        "    Client->>Server: Request\n"
        "    Server-->>Client: Response"
    )


def test_returns_empty_list_when_no_mermaid_diagrams_exist():
    content = (
        "# Architecture\n\n"
        "This document contains no Mermaid diagrams."
    )

    extractor = MermaidExtractor()

    diagrams = extractor.extract(content)

    assert diagrams == []


def test_ignores_non_mermaid_code_blocks():
    content = (
        "# Architecture\n\n"
        "```python\n"
        "print('hello')\n"
        "```\n\n"
        "```javascript\n"
        "console.log('hello');\n"
        "```\n\n"
        "```mermaid\n"
        "flowchart LR\n"
        "    A --> B\n"
        "```"
    )

    extractor = MermaidExtractor()

    diagrams = extractor.extract(content)

    assert len(diagrams) == 1
    assert diagrams[0].id == "diagram-1"
    assert diagrams[0].content == (
        "flowchart LR\n"
        "    A --> B"
    )


def test_preserves_diagram_content_formatting():
    content = (
        "```mermaid\n"
        "flowchart TD\n"
        "\n"
        "    A[Frontend]\n"
        "        --> B[Backend]\n"
        "\n"
        "    B --> C[AI Service]\n"
        "```"
    )

    extractor = MermaidExtractor()

    diagrams = extractor.extract(content)

    assert len(diagrams) == 1
    assert diagrams[0].content == (
        "flowchart TD\n"
        "\n"
        "    A[Frontend]\n"
        "        --> B[Backend]\n"
        "\n"
        "    B --> C[AI Service]"
    )