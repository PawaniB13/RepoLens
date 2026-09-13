import pytest

from generators.document_update_service import DocumentUpdateService
from models.response import SuggestedUpdate


def create_update(
    current_content: str,
    suggested_content: str,
    change_type: str = "MODIFY",
) -> SuggestedUpdate:
    return SuggestedUpdate(
        artifactType="README",
        artifactPath="README.md",
        changeType=change_type,
        section="Overview",
        currentContent=current_content,
        suggestedContent=suggested_content,
        explanation="The documented content is outdated.",
        confidence=0.95,
    )


def test_apply_replaces_exact_content_once():
    service = DocumentUpdateService()

    document = """# RepoLens

## Overview

RepoLens analyzes repositories manually.
"""

    update = create_update(
        current_content="RepoLens analyzes repositories manually.",
        suggested_content="RepoLens automatically analyzes repositories.",
    )

    result = service.apply(
        document_content=document,
        update=update,
    )

    assert result == """# RepoLens

## Overview

RepoLens automatically analyzes repositories.
"""


def test_apply_fails_when_current_content_is_missing():
    service = DocumentUpdateService()

    document = """# RepoLens

## Overview

Repository analysis service.
"""

    update = create_update(
        current_content="This content does not exist.",
        suggested_content="New content.",
    )

    with pytest.raises(
        ValueError,
        match="currentContent was not found",
    ):
        service.apply(
            document_content=document,
            update=update,
        )


def test_apply_fails_when_current_content_is_ambiguous():
    service = DocumentUpdateService()

    document = """# RepoLens

Repository analysis service.

## Details

Repository analysis service.
"""

    update = create_update(
        current_content="Repository analysis service.",
        suggested_content="Updated repository analysis service.",
    )

    with pytest.raises(
        ValueError,
        match="occurs multiple times",
    ):
        service.apply(
            document_content=document,
            update=update,
        )




def test_apply_is_safe_when_update_is_already_applied():
    service = DocumentUpdateService()

    document = """# RepoLens

## Overview

RepoLens automatically analyzes repositories.
"""

    update = create_update(
        current_content="RepoLens analyzes repositories manually.",
        suggested_content="RepoLens automatically analyzes repositories.",
    )

    with pytest.raises(
        ValueError,
        match="currentContent was not found",
    ):
        service.apply(
            document_content=document,
            update=update,
        )

def test_apply_creates_new_document():
    service = DocumentUpdateService()

    update = create_update(
        current_content="",
        suggested_content="# API Documentation\n\n## Endpoints",
        change_type="CREATE",
    )

    result = service.apply(
        document_content="",
        update=update,
    )

    assert result == "# API Documentation\n\n## Endpoints"

def test_apply_rejects_empty_artifact_path():
    service = DocumentUpdateService()

    update = SuggestedUpdate(
        artifactType="README",
        artifactPath="",
        changeType="MODIFY",
        section="Overview",
        currentContent="Old content.",
        suggestedContent="New content.",
        explanation="The documentation is outdated.",
        confidence=0.95,
    )

    with pytest.raises(
        ValueError,
        match="artifactPath must not be empty",
    ):
        service.apply(
            document_content="Old content.",
            update=update,
        )