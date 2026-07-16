"""AI analysis of feedback text using Claude (structured output)."""
from enum import Enum

import anthropic
from anthropic import AsyncAnthropic
from pydantic import BaseModel, Field

from app.core.config import settings

MODEL = "claude-haiku-4-5"

SYSTEM_PROMPT = (
    "You analyze customer feedback. Given a piece of text, classify its overall "
    "sentiment, extract the key topics as short labels, and write a one-sentence "
    "summary. Base everything only on the text provided."
)


class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class AnalysisResult(BaseModel):
    """Structured result the model must return."""

    sentiment: Sentiment
    topics: list[str] = Field(description="1-5 short topic labels mentioned in the text")
    summary: str = Field(description="A one-sentence summary of the feedback")


class AIServiceError(Exception):
    """Raised when the AI provider call fails."""


def _client() -> AsyncAnthropic:
    return AsyncAnthropic(api_key=settings.anthropic_api_key)


async def analyze_text(text: str) -> AnalysisResult:
    try:
        response = await _client().messages.parse(
            model=MODEL,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": text}],
            output_format=AnalysisResult,
        )
    except anthropic.AnthropicError as exc:
        raise AIServiceError("The AI analysis request failed") from exc

    return response.parsed_output