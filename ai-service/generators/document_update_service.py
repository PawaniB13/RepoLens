from models.response import SuggestedUpdate


class DocumentUpdateService:
    """
    Applies validated SuggestedUpdate instructions to engineering
    knowledge documents.

    This service is deterministic and does not:
    - perform LLM inference
    - detect drift
    - generate suggestions
    - perform Git operations
    - communicate with GitHub
    - persist files

    It only transforms document content according to a validated
    SuggestedUpdate.
    """

    def apply(
        self,
        document_content: str,
        update: SuggestedUpdate,
    ) -> str:
        """
        Apply a suggested update to document content.

        MODIFY updates require the currentContent to exist exactly
        once in the target document. This prevents accidental
        replacement of the wrong content.

        CREATE updates require an empty target document and return
        the complete suggested content.
        """

        if not update.artifactPath.strip():
            raise ValueError(
                "artifactPath must not be empty."
            )

        if update.changeType == "CREATE":
            if not update.suggestedContent:
                raise ValueError(
                    "suggestedContent must not be empty for a CREATE update."
                )

            if document_content:
                raise ValueError(
                    "CREATE update cannot be applied to an existing document."
                )

            return update.suggestedContent

        if not update.currentContent:
            raise ValueError(
                "currentContent must not be empty for a MODIFY update."
            )

        occurrence_count = document_content.count(
            update.currentContent
        )

        if occurrence_count == 0:
            raise ValueError(
                "The expected currentContent was not found "
                "in the target document."
            )

        if occurrence_count > 1:
            raise ValueError(
                "The expected currentContent occurs multiple times "
                "in the target document."
            )

        return document_content.replace(
            update.currentContent,
            update.suggestedContent,
            1,
        )