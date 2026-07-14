"""Business logic for analyses.

For Phase 1 the data lives in memory. In Phase 2 this layer will be rewritten
to talk to PostgreSQL, while the router above it stays unchanged.
"""
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.analysis import Analysis, AnalysisCreate


class AnalysisService:
    def __init__(self) -> None:
        self._items: dict[UUID, Analysis] = {}

    def create(self, data: AnalysisCreate) -> Analysis:
        analysis = Analysis(
            id=uuid4(),
            text=data.text,
            created_at=datetime.now(timezone.utc),
        )
        self._items[analysis.id] = analysis
        return analysis

    def list_all(self) -> list[Analysis]:
        return list(self._items.values())

    def get(self, analysis_id: UUID) -> Analysis | None:
        return self._items.get(analysis_id)

    def delete(self, analysis_id: UUID) -> bool:
        return self._items.pop(analysis_id, None) is not None


service = AnalysisService()