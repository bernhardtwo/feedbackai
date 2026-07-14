"""Application entrypoint: creates the FastAPI app and wires routers."""
from fastapi import FastAPI

from app.routers import analyses

app = FastAPI(title="FeedbackAI", version="0.1.0")

app.include_router(analyses.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}