from tree_sitter import Node

from analyzers.parser import ParserFactory
from models.code_facts import (
    CodeClass,
    CodeEndpoint,
    CodeFacts,
    CodeFunction,
    CodeImport,
    CodeMethod,
)


class PythonAnalyzer:
    """
    Extracts deterministic structural facts from Python source code.

    This analyzer is responsible only for Python-specific syntax.
    It does not perform semantic interpretation or drift detection.
    """

    LANGUAGE = "python"

    def __init__(self) -> None:
        self._parser = ParserFactory.create(self.LANGUAGE)

    def analyze(self, filename: str, source_code: str) -> CodeFacts:
        """Parse Python source code and return deterministic CodeFacts."""

        source_bytes = source_code.encode("utf-8")
        tree = self._parser.parse(source_bytes)

        facts = CodeFacts(
            filename=filename,
            language=self.LANGUAGE,
            line_count=len(source_code.splitlines()),
            file_size_bytes=len(source_bytes),
        )

        if tree.root_node.has_error:
            facts.parse_status = "parse_error"
            facts.parse_error = "Tree-sitter detected syntax errors."
            return facts

        self._extract_node(
            node=tree.root_node,
            source_bytes=source_bytes,
            facts=facts,
            current_class=None,
        )

        facts.parse_status = "success"
        return facts

    def _extract_node(
        self,
        node: Node,
        source_bytes: bytes,
        facts: CodeFacts,
        current_class: str | None,
    ) -> None:
        """Recursively traverse the syntax tree and extract structural facts."""

        next_class = current_class

        if node.type == "class_definition":
            name_node = node.child_by_field_name("name")

            if name_node is not None:
                class_name = self._node_text(name_node, source_bytes)

                facts.classes.append(
                    CodeClass(
                        name=class_name,
                        line_start=node.start_point.row + 1,
                        line_end=node.end_point.row + 1,
                    )
                )

                next_class = class_name

        elif node.type == "decorated_definition":
            self._extract_endpoint(
                node=node,
                source_bytes=source_bytes,
                facts=facts,
            )

        elif node.type == "function_definition":
            name_node = node.child_by_field_name("name")

            if name_node is not None:
                function_name = self._node_text(name_node, source_bytes)

                if current_class is not None:
                    facts.methods.append(
                        CodeMethod(
                            class_name=current_class,
                            method_name=function_name,
                            line_start=node.start_point.row + 1,
                            line_end=node.end_point.row + 1,
                        )
                    )
                else:
                    facts.functions.append(
                        CodeFunction(
                            name=function_name,
                            line_start=node.start_point.row + 1,
                            line_end=node.end_point.row + 1,
                        )
                    )

        elif node.type in {"import_statement", "import_from_statement"}:
            self._extract_import(node, source_bytes, facts)

        for child in node.children:
            self._extract_node(
                node=child,
                source_bytes=source_bytes,
                facts=facts,
                current_class=next_class,
            )

    def _extract_endpoint(
        self,
        node: Node,
        source_bytes: bytes,
        facts: CodeFacts,
    ) -> None:
        """Extract FastAPI-style HTTP endpoints from decorators."""

        function_node = None

        for child in node.named_children:
            if child.type in {
                "function_definition",
                "async_function_definition",
            }:
                function_node = child
                break

        if function_node is None:
            return

        name_node = function_node.child_by_field_name("name")

        if name_node is None:
            return

        handler_name = self._node_text(name_node, source_bytes)

        for child in node.named_children:
            if child.type != "decorator":
                continue

            endpoint = self._parse_fastapi_decorator(
                decorator_node=child,
                source_bytes=source_bytes,
            )

            if endpoint is None:
                continue

            method, path = endpoint

            facts.api_endpoints.append(
                CodeEndpoint(
                    method=method,
                    path=path,
                    handler_name=handler_name,
                    line_start=node.start_point.row + 1,
                    line_end=node.end_point.row + 1,
                )
            )

    def _parse_fastapi_decorator(
        self,
        decorator_node: Node,
        source_bytes: bytes,
    ) -> tuple[str, str] | None:
        """Extract HTTP method and path from a FastAPI route decorator."""

        for child in decorator_node.named_children:
            if child.type != "call":
                continue

            function_node = child.child_by_field_name("function")

            if function_node is None:
                continue

            function_name = ""

            if function_node.type == "attribute":
                attribute_node = function_node.child_by_field_name(
                    "attribute"
                )

                if attribute_node is not None:
                    function_name = self._node_text(
                        attribute_node,
                        source_bytes,
                    )

            elif function_node.type == "identifier":
                function_name = self._node_text(
                    function_node,
                    source_bytes,
                )

            http_methods = {
                "get",
                "post",
                "put",
                "patch",
                "delete",
            }

            if function_name.lower() not in http_methods:
                continue

            arguments_node = child.child_by_field_name("arguments")

            if arguments_node is None:
                continue

            for argument in arguments_node.named_children:
                if argument.type != "string":
                    continue

                path = self._node_text(argument, source_bytes)

                if len(path) >= 2 and path[0] in {"'", '"'}:
                    path = path[1:-1]

                return function_name.upper(), path

        return None

    def _extract_import(
        self,
        node: Node,
        source_bytes: bytes,
        facts: CodeFacts,
    ) -> None:
        """Extract a Python import statement."""

        statement = self._node_text(node, source_bytes)

        if node.type == "import_from_statement":
            module_part = statement[len("from "):].split(
                " import ",
                maxsplit=1,
            )[0].strip()

            if module_part.startswith("."):
                package = module_part
            else:
                package = module_part.split(".", maxsplit=1)[0]

        else:
            name_node = node.child_by_field_name("name")

            package = (
                self._node_text(name_node, source_bytes)
                if name_node is not None
                else ""
            )

        facts.imports.append(
            CodeImport(
                statement=statement,
                package=package,
                line=node.start_point.row + 1,
            )
        )

    @staticmethod
    def _node_text(node: Node, source_bytes: bytes) -> str:
        """Return the source text represented by a Tree-sitter node."""

        return source_bytes[
            node.start_byte:node.end_byte
        ].decode("utf-8")