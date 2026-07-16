"""Async test fixtures: a client wired to a fresh test database per test."""
# tests/conftest.py
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.analysis import Analysis  # noqa: F401
from app.models.topic import Topic  # noqa: F401
from app.services.ai_service import AnalysisResult, Sentiment


@pytest.fixture(autouse=True)
def mock_ai():
    fake = AnalysisResult(
        sentiment=Sentiment.positive,
        topics=["quality", "price"],
        summary="The customer was happy.",
    )
    with patch("app.routers.analyses.analyze_text", AsyncMock(return_value=fake)):
        yield


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    engine = create_async_engine(settings.test_database_url, poolclass=NullPool)
    TestSession = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
    await engine.dispose()