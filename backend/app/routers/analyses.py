"""HTTP routes for the /analyses resource."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import Analysis, AnalysisCreate
from app.services import analysis_service

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=Analysis, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    payload: AnalysisCreate, db: AsyncSession = Depends(get_db)
) -> Analysis:
    return await analysis_service.create(db, payload)


@router.get("", response_model=list[Analysis])
async def list_analyses(db: AsyncSession = Depends(get_db)) -> list[Analysis]:
    return await analysis_service.list_all(db)


@router.get("/{analysis_id}", response_model=Analysis)
async def get_analysis(
    analysis_id: UUID, db: AsyncSession = Depends(get_db)
) -> Analysis:
    analysis = await analysis_service.get(db, analysis_id)
    if analysis is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    analysis_id: UUID, db: AsyncSession = Depends(get_db)
) -> None:
    deleted = await analysis_service.remove(db, analysis_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Analysis not found")