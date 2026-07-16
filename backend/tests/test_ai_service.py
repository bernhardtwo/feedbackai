"""Tests for the AI service, with the Anthropic client fully mocked."""
from unittest.mock import AsyncMock, MagicMock, patch

import anthropic
import pytest

from app.services.ai_service import (
    AIServiceError,
    AnalysisResult,
    Sentiment,
    analyze_text,
)


async def test_analyze_text_returns_parsed_result() -> None:
    fake = AnalysisResult(
        sentiment=Sentiment.positive,
        topics=["quality", "price"],
        summary="The customer loved the product.",
    )
    fake_response = MagicMock()
    fake_response.parsed_output = fake

    mock_client = MagicMock()
    mock_client.messages.parse = AsyncMock(return_value=fake_response)

    with patch("app.services.ai_service._client", return_value=mock_client):
        result = await analyze_text("Great quality for the price!")

    assert result.sentiment == Sentiment.positive
    assert "quality" in result.topics
    assert result.summary == "The customer loved the product."


async def test_analyze_text_wraps_provider_errors() -> None:
    mock_client = MagicMock()
    mock_client.messages.parse = AsyncMock(
        side_effect=anthropic.AnthropicError("provider down")
    )

    with patch("app.services.ai_service._client", return_value=mock_client):
        with pytest.raises(AIServiceError):
            await analyze_text("anything")