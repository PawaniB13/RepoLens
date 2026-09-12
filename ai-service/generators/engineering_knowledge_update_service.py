from generators.document_update_service import DocumentUpdateService
from generators.mermaid_extractor import MermaidExtractor
from models.requests import CurrentEngineeringKnowledge
from models.response import SuggestedUpdate


class EngineeringKnowledgeUpdateService:
    """
    Applies generated updates to the supported engineering knowledge
    artifacts contained in CurrentEngineeringKnowledge.

    This service is responsible for:
    - mapping artifact types to their corresponding documents
    - delegating content transformation to DocumentUpdateService
    - rebuilding Mermaid diagram metadata for architecture documentation

    This service does not:
    - perform LLM inference
    - detect drift
    - generate update suggestions
    - perform Git operations
    - communicate with GitHub
    - persist files
    """

    def __init__(
        self,
        document_update_service: DocumentUpdateService,
        mermaid_extractor: MermaidExtractor,
    ) -> None:
        self._document_update_service = document_update_service
        self._mermaid_extractor = mermaid_extractor

    def apply_updates(
        self,
        knowledge: CurrentEngineeringKnowledge,
        updates: list[SuggestedUpdate],
    ) -> CurrentEngineeringKnowledge:
        """
        Apply all suggested updates to the corresponding engineering
        knowledge artifacts.

        The original knowledge model is not modified in place.
        A new CurrentEngineeringKnowledge instance is returned.

        Architecture documentation Mermaid metadata is rebuilt
        whenever the architecture document is updated.
        """

        updated_knowledge = knowledge.model_copy(deep=True)

        architecture_updated = False

        for update in updates:
            if update.artifactType == "README":
                updated_knowledge.readme.content = (
                    self._document_update_service.apply(
                        document_content=updated_knowledge.readme.content,
                        update=update,
                    )
                )

            elif update.artifactType == "ARCHITECTURE":
                updated_knowledge.architectureDocumentation.content = (
                    self._document_update_service.apply(
                        document_content=(
                            updated_knowledge
                            .architectureDocumentation
                            .content
                        ),
                        update=update,
                    )
                )

                architecture_updated = True

            elif update.artifactType == "API_DOCUMENTATION":
                updated_knowledge.apiDocumentation.content = (
                    self._document_update_service.apply(
                        document_content=(
                            updated_knowledge
                            .apiDocumentation
                            .content
                        ),
                        update=update,
                    )
                )

            else:
                raise ValueError(
                    "Unsupported engineering knowledge artifact: "
                    f"{update.artifactType}"
                )

        if architecture_updated:
            updated_knowledge.architectureDocumentation.mermaidDiagrams = (
                self._mermaid_extractor.extract(
                    updated_knowledge
                    .architectureDocumentation
                    .content
                )
            )

        return updated_knowledge