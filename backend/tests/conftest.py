"""Shared pytest fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.analysis_service import service


@pytest.fixture
def client() -> TestClient:
    """A test client that drives the app without a running server."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_store() -> None:
    """Clear the in-memory store before each test to keep tests isolated."""
    service._items.clear()
    yield