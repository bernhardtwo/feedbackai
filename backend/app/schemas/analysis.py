"""Pydantic schemas for the Analysis resource.

Schemas define the shape of data crossing the API boundary: FastAPI uses them
to validate incoming requests and to serialize outgoing responses.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    """Input schema: what a client must send to create an analysis."""
    text: str = Field(min_length=1, max_length=5000)


class Analysis(BaseModel):
    """Output schema: what the API returns for an analysis."""
    id: UUID
    text: str
    created_at: datetime