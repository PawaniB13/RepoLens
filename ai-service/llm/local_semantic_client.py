import re

from llm.client import LLMClient
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)


class LocalSemanticClient(LLMClient):
    """
    Deterministic local implementation of LLMClient.

    This client provides a quota-free semantic-analysis path for
    development and demonstrations.

    It uses deterministic repository context and extracted CodeFacts
    rather than an external LLM.

    It does not:
    - call external APIs
    - perform Git operations
    - generate documentation updates
    - mutate engineering knowledge
    """

    def analyze(
        self,
        context: dict,
    ) -> SemanticAnalysisResult:
        api_drift, api_reason, api_confidence = (
            self._analyze_api_documentation(context)
        )

        readme_drift, readme_reason, readme_confidence = (
            self._analyze_readme(context)
        )

        architecture_drift, architecture_reason, architecture_confidence = (
            self._analyze_architecture(context)
        )

        return SemanticAnalysisResult(
            artifacts=[
                SemanticArtifactAnalysis(
                    artifactType="README",
                    driftDetected=readme_drift,
                    reason=readme_reason,
                    confidence=readme_confidence,
                ),
                SemanticArtifactAnalysis(
                    artifactType="ARCHITECTURE",
                    driftDetected=architecture_drift,
                    reason=architecture_reason,
                    confidence=architecture_confidence,
                ),
                SemanticArtifactAnalysis(
                    artifactType="API_DOCUMENTATION",
                    driftDetected=api_drift,
                    reason=api_reason,
                    confidence=api_confidence,
                ),
            ]
        )

    def _analyze_api_documentation(
        self,
        context: dict,
    ) -> tuple[bool, str, float]:
        endpoints = self._extract_api_endpoints(context)

        documentation = (
            context
            .get("currentEngineeringKnowledge", {})
            .get("apiDocumentation", {})
            .get("content", "")
        )

        if not endpoints:
            return (
                False,
                "No API endpoints were identified in the analyzed "
                "source files.",
                0.95,
            )

        undocumented_endpoints = [
            endpoint
            for endpoint in endpoints
            if not self._endpoint_documented(
                endpoint["method"],
                endpoint["path"],
                documentation,
            )
        ]

        if not undocumented_endpoints:
            return (
                False,
                "All analyzed API endpoints are represented in "
                "the current API documentation.",
                0.95,
            )

        endpoint_names = ", ".join(
            f"{endpoint['method']} {endpoint['path']}"
            for endpoint in undocumented_endpoints
        )

        return (
            True,
            (
                "The current API documentation does not describe "
                f"the following analyzed endpoint(s): {endpoint_names}."
            ),
            0.98,
        )

    def _analyze_readme(
        self,
        context: dict,
    ) -> tuple[bool, str, float]:
        endpoints = self._extract_api_endpoints(context)

        readme = (
            context
            .get("currentEngineeringKnowledge", {})
            .get("readme", {})
            .get("content", "")
        )

        if not endpoints:
            return (
                False,
                "No API endpoints were identified that require "
                "README comparison.",
                0.90,
            )

        undocumented_endpoints = [
            endpoint
            for endpoint in endpoints
            if not self._endpoint_documented(
                endpoint["method"],
                endpoint["path"],
                readme,
            )
        ]

        if not undocumented_endpoints:
            return (
                False,
                "The README represents the analyzed API endpoints.",
                0.92,
            )

        endpoint_names = ", ".join(
            f"{endpoint['method']} {endpoint['path']}"
            for endpoint in undocumented_endpoints
        )

        return (
            True,
            (
                "The README does not document the following analyzed "
                f"endpoint(s): {endpoint_names}."
            ),
            0.94,
        )

    def _analyze_architecture(
        self,
        context: dict,
    ) -> tuple[bool, str, float]:
        """
        Perform conservative architecture analysis.

        Architecture drift is reported only when repository metadata
        explicitly identifies an architecture type and the architecture
        documentation explicitly describes a conflicting architecture.
        """

        architecture = (
            context
            .get("currentEngineeringKnowledge", {})
            .get("architectureDocumentation", {})
            .get("content", "")
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

        if not architecture:
            return (
                False,
                "Architecture documentation is empty and the local "
                "analysis does not have sufficient evidence to "
                "construct a trustworthy architecture update.",
                0.85,
            )

        if not architecture_type:
            return (
                False,
                "Repository architecture type metadata is unavailable; "
                "no deterministic architectural inconsistency was "
                "established.",
                0.85,
            )

        documented_architecture = self._classify_architecture(
            architecture
        )

        metadata_architecture = self._classify_architecture(
            architecture_type
        )

        if (
            documented_architecture is None
            or metadata_architecture is None
        ):
            return (
                False,
                "No deterministic architectural inconsistency was "
                "established from the available architecture facts.",
                0.85,
            )

        if documented_architecture == metadata_architecture:
            return (
                False,
                (
                    "The architecture documentation is consistent "
                    "with the repository architecture type."
                ),
                0.95,
            )

        return (
            True,
            (
                "The architecture documentation describes a "
                f"{documented_architecture} architecture, while "
                f"repository metadata identifies the architecture "
                f"as {metadata_architecture}."
            ),
            0.97,
        )

    def _classify_architecture(
        self,
        text: str,
    ) -> str | None:
        """
        Classify only explicitly recognizable architecture categories.

        Returns None when the available text is too ambiguous.
        """

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
                r"\bevent driven\b",
            ),
            "client-server": (
                r"\bclient[- ]server\b",
                r"\bclient server\b",
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

                endpoints.append(
                    {
                        "method": method,
                        "path": path,
                    }
                )

        return self._deduplicate_endpoints(endpoints)

    def _endpoint_documented(
        self,
        method: str,
        path: str,
        documentation: str,
    ) -> bool:
        normalized_documentation = documentation.lower()

        normalized_method = method.lower()
        normalized_path = path.lower()

        method_present = re.search(
            rf"\b{re.escape(normalized_method)}\b",
            normalized_documentation,
        )

        path_present = normalized_path in normalized_documentation

        return bool(method_present and path_present)

    def _deduplicate_endpoints(
        self,
        endpoints: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        unique_endpoints: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()

        for endpoint in endpoints:
            key = (
                endpoint["method"],
                endpoint["path"],
            )

            if key in seen:
                continue

            seen.add(key)
            unique_endpoints.append(endpoint)

        return unique_endpoints