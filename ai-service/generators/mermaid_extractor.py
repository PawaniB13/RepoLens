from models.requests import MermaidDiagram


class MermaidExtractor:
    """
    Extracts Mermaid diagrams from architecture documentation.

    This component is deterministic and does not:
    - perform LLM inference
    - interpret diagram meaning
    - generate diagrams
    - modify documentation
    - perform Git operations
    - communicate with GitHub

    It only extracts Mermaid code blocks from Markdown content.
    """

    def extract(
        self,
        document_content: str,
    ) -> list[MermaidDiagram]:
        """
        Extract Mermaid code blocks from Markdown content.

        Each Mermaid fenced code block becomes one MermaidDiagram.

        Diagram IDs are generated deterministically according to
        their order in the document.
        """

        diagrams: list[MermaidDiagram] = []

        lines = document_content.splitlines()

        inside_mermaid = False
        current_lines: list[str] = []

        for line in lines:
            stripped = line.strip()

            if not inside_mermaid:
                if stripped == "```mermaid":
                    inside_mermaid = True
                    current_lines = []

                continue

            if stripped == "```":
                diagrams.append(
                    MermaidDiagram(
                        id=f"diagram-{len(diagrams) + 1}",
                        type="mermaid",
                        content="\n".join(current_lines),
                    )
                )

                inside_mermaid = False
                current_lines = []

                continue

            current_lines.append(line)

        return diagrams