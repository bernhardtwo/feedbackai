"""Business logic for analyses, backed by PostgreSQL."""
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.analysis import Analysis
from app.models.topic import Topic
from app.services.ai_service import AnalysisResult


async def create(db: AsyncSession, text: str, result: AnalysisResult) -> Analysis:
    analysis = Analysis(
        text=text,
        sentiment=result.sentiment.value,
        summary=result.summary,
        topics=[Topic(name=name) for name in result.topics],
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis, attribute_names=["created_at"])
    return analysis


async def list_all(db: AsyncSession) -> list[Analysis]:
    result = await db.execute(
        select(Analysis)
        .options(selectinload(Analysis.topics))
        .order_by(Analysis.created_at)
    )
    return list(result.scalars().all())


async def get(db: AsyncSession, analysis_id: UUID) -> Analysis | None:
    result = await db.execute(
        select(Analysis)
        .options(selectinload(Analysis.topics))
        .where(Analysis.id == analysis_id)
    )
    return result.scalar_one_or_none()


async def remove(db: AsyncSession, analysis_id: UUID) -> bool:
    result = await db.execute(delete(Analysis).where(Analysis.id == analysis_id))
    await db.commit()
    return result.rowcount > 0