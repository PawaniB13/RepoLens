import re

from generators.llm_update_generator import UpdateGenerationClient
from models.response import SuggestedUpdate
from models.semantic_analysis import SemanticAnalysisResult


class LocalUpdateClient(UpdateGenerationClient):
    """
    Deterministic local implementation of UpdateGenerationClient.

    Provides a quota-free documentation-update path for development
    and demonstrations.

    It generates updates only from deterministic repository context
    and existing engineering-knowledge documents.
    """

    def generate_updates(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        updates: list[SuggestedUpdate] = []

        affected_artifacts = {
            artifact.artifactType
            for artifact in semantic_analysis.artifacts
            if artifact.driftDetected
        }

        if "README" in affected_artifacts:
            endpoints = self._extract_api_endpoints(context)

            if endpoints:
                update = self._build_readme_update(
                    context=context,
                    endpoints=endpoints,
                )

                if update is not None:
                    updates.append(update)

        if "API_DOCUMENTATION" in affected_artifacts:
            endpoints = self._extract_api_endpoints(context)

            if endpoints:
                update = self._build_api_documentation_update(
                    context=context,
                    endpoints=endpoints,
                )

                if update is not None:
                    updates.append(update)

        if "ARCHITECTURE" in affected_artifacts:
            update = self._build_architecture_update(
                context=context,
            )

            if update is not None:
                updates.append(update)

        return updates

    def _build_readme_update(
        self,
        context: dict,
        endpoints: list[dict[str, str]],
    ) -> SuggestedUpdate | None:
        readme = (
            context
            .get("currentEngineeringKnowledge", {})
            .get("readme", {})
        )

        current_content = readme.get("content", "")
        artifact_path = readme.get("path", "README.md")

        missing_endpoints = [
            endpoint
            for endpoint in endpoints
            if not self._endpoint_documented(
                endpoint["method"],
                endpoint["path"],
                current_content,
            )
        ]

        if not missing_endpoints:
            return None

        suggested_content = self._update_readme_endpoint_section(
            current_content=current_content,
            missing_endpoints=missing_endpoints,
        )

        return SuggestedUpdate(
            artifactType="README",
            artifactPath=artifact_path,
            changeType=(
                "MODIFY"
                if current_content.strip()
                else "CREATE"
            ),
            section="Endpoints",
            currentContent=current_content,
            suggestedContent=suggested_content,
            explanation=(
                "The README does not document one or more API "
                "endpoints identified from the changed source code."
            ),
            confidence=0.94,
        )

    def _update_readme_endpoint_section(
        self,
        current_content: str,
        missing_endpoints: list[dict[str, str]],
    ) -> str:
        endpoint_lines = "\n".join(
            self._format_readme_endpoint(endpoint)
            for endpoint in missing_endpoints
        )

        if not current_content.strip():
            return (
                "# API Endpoints\n\n"
                "## Endpoints\n\n"
                f"{endpoint_lines}\n"
            )

        section_match = re.search(
            r"(?im)^##\s+Endpoints\s*$",
            current_content,
        )

        if section_match:
            section_start = section_match.end()

            next_section_match = re.search(
                r"(?m)^##\s+",
                current_content[section_start:],
            )

            if next_section_match:
                section_end = (
                    section_start
                    + next_section_match.start()
                )
            else:
                section_end = len(current_content)

            existing_section = current_content[
                section_start:section_end
            ].strip()

            updated_section = (
                "\n\n"
                + existing_section
                + "\n"
                + endpoint_lines
                + "\n"
            )

            return (
                current_content[:section_start]
                + updated_section
                + current_content[section_end:]
            )

        return (
            current_content.rstrip()
            + "\n\n"
            + "## Endpoints\n\n"
            + endpoint_lines
            + "\n"
        )

    def _build_api_documentation_update(
        self,
        context: dict,
        endpoints: list[dict[str, str]],
    ) -> SuggestedUpdate | None:
        api_documentation = (
            context
            .get("currentEngineeringKnowledge", {})
            .get("apiDocumentation", {})
        )

        current_content = api_documentation.get("content", "")
        artifact_path = api_documentation.get(
            "path",
            "docs/api.md",
        )

        missing_endpoints = [
            endpoint
            for endpoint in endpoints
            if not self._endpoint_documented(
                endpoint["method"],
                endpoint["path"],
                current_content,
            )
        ]

        if not missing_endpoints:
            return None

        endpoint_sections = "\n\n".join(
            self._format_api_endpoint_section(endpoint)
            for endpoint in missing_endpoints
        )

        if current_content.strip():
            suggested_content = (
                current_content.rstrip()
                + "\n\n"
                + endpoint_sections
                + "\n"
            )

            change_type = "MODIFY"
        else:
            suggested_content = endpoint_sections + "\n"
            change_type = "CREATE"

        return SuggestedUpdate(
            artifactType="API_DOCUMENTATION",
            artifactPath=artifact_path,
            changeType=change_type,
            section=None,
            currentContent=current_content,
            suggestedContent=suggested_content,
            explanation=(
                "The API documentation does not describe one or more "
                "API endpoints identified from the changed source code."
            ),
            confidence=0.98,
        )

    def _build_architecture_update(
        self,
        context: dict,
    ) -> SuggestedUpdate | None:
        engineering_knowledge = context.get(
            "currentEngineeringKnowledge",
            {},
        )

        architecture_documentation = engineering_knowledge.get(
            "architectureDocumentation",
            {},
        )

        current_content = architecture_documentation.get(
            "content",
            "",
        )

        artifact_path = architecture_documentation.get(
            "path",
            "docs/architecture.md",
        )

        repository_metadata = context.get(
            "repositoryMetadata",
            {},
        )

        architecture_type = str(
            repository_metadata.get(
                "architectureType",
                "",
            )
        ).strip()

        if not architecture_type:
            return None

        normalized_architecture_type = (
            self._normalize_architecture_type(
                architecture_type
            )
        )

        if normalized_architecture_type is None:
            return None

        documented_architecture = self._classify_architecture(
            current_content
        )

        if (
            documented_architecture is not None
            and documented_architecture
            == normalized_architecture_type
        ):
            return None

        suggested_content = self._build_architecture_content(
            current_content=current_content,
            architecture_type=normalized_architecture_type,
            context=context,
        )

        return SuggestedUpdate(
            artifactType="ARCHITECTURE",
            artifactPath=artifact_path,
            changeType=(
                "MODIFY"
                if current_content.strip()
                else "CREATE"
            ),
            section="Architecture",
            currentContent=current_content,
            suggestedContent=suggested_content,
            explanation=(
                "The architecture documentation conflicts with the "
                "explicit repository architecture type metadata."
            ),
            confidence=0.95,
        )

    def _build_architecture_content(
        self,
        current_content: str,
        architecture_type: str,
        context: dict,
    ) -> str:
        architecture_description = (
            f"The application follows a "
            f"{architecture_type} architecture."
        )

        mermaid_diagram = self._build_mermaid_diagram(
            architecture_type=architecture_type,
            context=context,
        )

        if not current_content.strip():
            return (
                "# Architecture\n\n"
                f"{architecture_description}\n\n"
                "```mermaid\n"
                f"{mermaid_diagram}\n"
                "```\n"
            )

        architecture_section_match = re.search(
            r"(?im)^#\s+Architecture\s*$",
            current_content,
        )

        if architecture_section_match:
            section_start = architecture_section_match.end()

            next_heading_match = re.search(
                r"(?m)^#\s+",
                current_content[section_start:],
            )

            if next_heading_match:
                section_end = (
                    section_start
                    + next_heading_match.start()
                )
            else:
                section_end = len(current_content)

            replacement = (
                "\n\n"
                f"{architecture_description}\n\n"
                "```mermaid\n"
                f"{mermaid_diagram}\n"
                "```\n"
            )

            return (
                current_content[:section_start]
                + replacement
                + current_content[section_end:]
            )

        return (
            current_content.rstrip()
            + "\n\n"
            + "# Architecture\n\n"
            + architecture_description
            + "\n\n"
            + "```mermaid\n"
            + mermaid_diagram
            + "\n```\n"
        )

    def _build_mermaid_diagram(
        self,
        architecture_type: str,
        context: dict,
    ) -> str:
        changed_files = context.get(
            "changedCodeFiles",
            [],
        )

        endpoint_count = len(
            self._extract_api_endpoints(context)
        )

        if architecture_type == "monolith":
            return (
                "flowchart TD\n"
                "    Client --> Application\n"
                "    Application --> API\n"
                f"    API --> Endpoints[{endpoint_count} API Endpoints]"
            )

        if architecture_type == "microservices":
            return (
                "flowchart TD\n"
                "    Client --> Gateway\n"
                "    Gateway --> Services\n"
                "    Services --> DataStore"
            )

        if architecture_type == "serverless":
            return (
                "flowchart TD\n"
                "    Client --> Functions\n"
                "    Functions --> DataStore"
            )

        if architecture_type == "event-driven":
            return (
                "flowchart TD\n"
                "    Producer --> EventBus\n"
                "    EventBus --> Consumer\n"
                "    Consumer --> DataStore"
            )

        if architecture_type == "layered":
            return (
                "flowchart TD\n"
                "    Presentation --> Business\n"
                "    Business --> DataAccess\n"
                "    DataAccess --> Database"
            )

        if architecture_type == "client-server":
            return (
                "flowchart TD\n"
                "    Client --> Server\n"
                "    Server --> Database"
            )

        file_count = len(changed_files)

        return (
            "flowchart TD\n"
            f"    Repository --> Application\n"
            f"    Application --> ChangedFiles[{file_count} Changed Files]"
        )

    def _normalize_architecture_type(
        self,
        architecture_type: str,
    ) -> str | None:
        normalized = architecture_type.lower()

        if "microservice" in normalized:
            return "microservices"

        if "monolith" in normalized:
            return "monolith"

        if "serverless" in normalized:
            return "serverless"

        if "event-driven" in normalized or "event driven" in normalized:
            return "event-driven"

        if "layered" in normalized:
            return "layered"

        if "client-server" in normalized or "client server" in normalized:
            return "client-server"

        return None

    def _classify_architecture(
        self,
        text: str,
    ) -> str | None:
        normalized_text = text.lower()

        architecture_patterns = {
            "microservices": (
                r"\bmicroservices?\b",
                r"\bmicro-services?\b",
            ),
            "monolith": (
                r"\bmonolith(?:ic)?\b",
            ),
            "serverless": (
                r"\bserverless\b",
            ),
            "layered": (
                r"\blayered architecture\b",
                r"\blayered application\b",
            ),
            "event-driven": (
                r"\bevent[- ]driven\b",
            ),
            "client-server": (
                r"\bclient[- ]server\b",
            ),
        }

        for architecture_name, patterns in architecture_patterns.items():
            if any(
                re.search(pattern, normalized_text)
                for pattern in patterns
            ):
                return architecture_name

        return None

    def _extract_api_endpoints(
        self,
        context: dict,
    ) -> list[dict[str, str]]:
        endpoints: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()

        for changed_file in context.get("changedCodeFiles", []):
            code_facts = changed_file.get("codeFacts", {})

            for endpoint in code_facts.get("api_endpoints", []):
                method = str(
                    endpoint.get("method", "")
                ).upper().strip()

                path = str(
                    endpoint.get("path", "")
                ).strip()

                if not method or not path:
                    continue

                key = (method, path)

                if key in seen:
                    continue

                seen.add(key)

                endpoints.append(
                    {
                        "method": method,
                        "path": path,
                    }
                )

        return endpoints

    def _endpoint_documented(
        self,
        method: str,
        path: str,
        documentation: str,
    ) -> bool:
        normalized_documentation = documentation.lower()

        method_pattern = rf"\b{re.escape(method.lower())}\b"

        method_present = re.search(
            method_pattern,
            normalized_documentation,
        )

        path_present = path.lower() in normalized_documentation

        return bool(method_present and path_present)

    def _format_readme_endpoint(
        self,
        endpoint: dict[str, str],
    ) -> str:
        return (
            f"- **{endpoint['method']} {endpoint['path']}** — "
            "API endpoint identified from the source code."
        )

    def _format_api_endpoint_section(
        self,
        endpoint: dict[str, str],
    ) -> str:
        return (
            f"## {endpoint['method']} {endpoint['path']}\n\n"
            "API endpoint identified from the source code."
        )