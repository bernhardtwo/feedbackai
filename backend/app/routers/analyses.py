"""HTTP routes for the /analyses resource."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.analysis import Analysis, AnalysisCreate
from app.services.analysis_service import service

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=Analysis, status_code=status.HTTP_201_CREATED)
async def create_analysis(payload: AnalysisCreate) -> Analysis:
    return service.create(payload)


@router.get("", response_model=list[Analysis])
async def list_analyses() -> list[Analysis]:
    return service.list_all()


@router.get("/{analysis_id}", response_model=Analysis)
async def get_analysis(analysis_id: UUID) -> Analysis:
    analysis = service.get(analysis_id)
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )
    return analysis


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(analysis_id: UUID) -> None:
    deleted = service.delete(analysis_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )