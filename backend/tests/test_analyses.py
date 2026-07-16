"""Tests for the /analyses endpoints against a real database."""
import uuid

from httpx import AsyncClient


async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_analysis_returns_201(client: AsyncClient) -> None:
    response = await client.post("/analyses", json={"text": "This product is great"})
    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "This product is great"
    assert "id" in body
    assert "created_at" in body


async def test_create_with_empty_text_returns_422(client: AsyncClient) -> None:
    response = await client.post("/analyses", json={"text": ""})
    assert response.status_code == 422


async def test_list_returns_all_created_items(client: AsyncClient) -> None:
    await client.post("/analyses", json={"text": "first"})
    await client.post("/analyses", json={"text": "second"})
    response = await client.get("/analyses")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_analysis_returns_the_item(client: AsyncClient) -> None:
    created = (await client.post("/analyses", json={"text": "find me"})).json()
    response = await client.get(f"/analyses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_get_missing_analysis_returns_404(client: AsyncClient) -> None:
    response = await client.get(f"/analyses/{uuid.uuid4()}")
    assert response.status_code == 404


async def test_delete_analysis_removes_it(client: AsyncClient) -> None:
    created = (await client.post("/analyses", json={"text": "delete me"})).json()
    assert (await client.delete(f"/analyses/{created['id']}")).status_code == 204
    assert (await client.get(f"/analyses/{created['id']}")).status_code == 404


async def test_delete_missing_analysis_returns_404(client: AsyncClient) -> None:
    response = await client.delete(f"/analyses/{uuid.uuid4()}")
    assert response.status_code == 404