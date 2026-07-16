"""Business logic for analyses, backed by PostgreSQL."""
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate


async def create(db: AsyncSession, data: AnalysisCreate) -> Analysis:
    analysis = Analysis(text=data.text)
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def list_all(db: AsyncSession) -> list[Analysis]:
    result = await db.execute(select(Analysis).order_by(Analysis.created_at))
    return list(result.scalars().all())


async def get(db: AsyncSession, analysis_id: UUID) -> Analysis | None:
    return await db.get(Analysis, analysis_id)


async def remove(db: AsyncSession, analysis_id: UUID) -> bool:
    result = await db.execute(delete(Analysis).where(Analysis.id == analysis_id))
    await db.commit()
    return result.rowcount > 0