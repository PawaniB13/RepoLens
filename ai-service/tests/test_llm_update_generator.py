from models.response import SuggestedUpdate
from models.semantic_analysis import (
    SemanticAnalysisResult,
    SemanticArtifactAnalysis,
)
from generators.llm_update_generator import (
    LLMUpdateGenerator,
    UpdateGenerationClient,
)


class FakeUpdateGenerationClient(UpdateGenerationClient):
    def __init__(
        self,
        updates: list[SuggestedUpdate],
    ) -> None:
        self.updates = updates
        self.called = False

    def generate_updates(
        self,
        context: dict,
        semantic_analysis: SemanticAnalysisResult,
    ) -> list[SuggestedUpdate]:
        self.called = True
        return self.updates


def test_no_drift_returns_empty_list_without_generation() -> None:
    client = FakeUpdateGenerationClient(
        updates=[]
    )

    generator = LLMUpdateGenerator(
        generation_client=client,
    )

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=False,
                reason="README is consistent with the repository.",
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="Architecture is consistent.",
                confidence=0.92,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation is consistent.",
                confidence=0.94,
            ),
        ]
    )

    result = generator.generate(
        context={"repository": "test"},
        semantic_analysis=semantic_analysis,
    )

    assert result == []
    assert client.called is False


def test_drift_generates_updates() -> None:
    expected_update = SuggestedUpdate(
        artifactType="README",
        artifactPath="README.md",
        changeType="MODIFY",
        section="Usage",
        currentContent="Old usage documentation.",
        suggestedContent="Updated usage documentation.",
        explanation="The documented usage no longer matches the current repository behavior.",
        confidence=0.91,
    )

    client = FakeUpdateGenerationClient(
        updates=[expected_update]
    )

    generator = LLMUpdateGenerator(
        generation_client=client,
    )

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README usage is outdated.",
                confidence=0.91,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="Architecture remains consistent.",
                confidence=0.90,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation remains consistent.",
                confidence=0.93,
            ),
        ]
    )

    result = generator.generate(
        context={"repository": "test"},
        semantic_analysis=semantic_analysis,
    )

    assert client.called is True
    assert result == [expected_update]

def test_drift_generator_rejects_update_for_unaffected_artifact() -> None:
    invalid_update = SuggestedUpdate(
        artifactType="ARCHITECTURE",
        artifactPath="docs/architecture.md",
        changeType="MODIFY",
        section="System Architecture",
        currentContent="Old architecture.",
        suggestedContent="Updated architecture.",
        explanation="Architecture changed.",
        confidence=0.90,
    )

    client = FakeUpdateGenerationClient(
        updates=[invalid_update]
    )

    generator = LLMUpdateGenerator(
        generation_client=client,
    )

    semantic_analysis = SemanticAnalysisResult(
        artifacts=[
            SemanticArtifactAnalysis(
                artifactType="README",
                driftDetected=True,
                reason="README is outdated.",
                confidence=0.91,
            ),
            SemanticArtifactAnalysis(
                artifactType="ARCHITECTURE",
                driftDetected=False,
                reason="Architecture remains consistent.",
                confidence=0.95,
            ),
            SemanticArtifactAnalysis(
                artifactType="API_DOCUMENTATION",
                driftDetected=False,
                reason="API documentation remains consistent.",
                confidence=0.94,
            ),
        ]
    )

    result = generator.generate(
        context={"repository": "test"},
        semantic_analysis=semantic_analysis,
    )

    assert result == []