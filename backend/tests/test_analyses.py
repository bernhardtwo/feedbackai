import uuid

from httpx import AsyncClient


async def test_create_returns_enriched_analysis(client: AsyncClient) -> None:
    response = await client.post("/analyses", json={"text": "Great quality, fair price"})
    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "Great quality, fair price"
    assert body["sentiment"] == "positive"
    assert body["summary"] == "The customer was happy."
    assert {t["name"] for t in body["topics"]} == {"quality", "price"}


async def test_create_with_empty_text_returns_422(client: AsyncClient) -> None:
    assert (await client.post("/analyses", json={"text": ""})).status_code == 422


async def test_list_includes_topics(client: AsyncClient) -> None:
    await client.post("/analyses", json={"text": "a"})
    await client.post("/analyses", json={"text": "b"})
    response = await client.get("/analyses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(len(item["topics"]) == 2 for item in data)


async def test_get_returns_the_item_with_topics(client: AsyncClient) -> None:
    created = (await client.post("/analyses", json={"text": "find me"})).json()
    response = await client.get(f"/analyses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert len(response.json()["topics"]) == 2


async def test_get_missing_returns_404(client: AsyncClient) -> None:
    assert (await client.get(f"/analyses/{uuid.uuid4()}")).status_code == 404


async def test_delete_removes_item_and_topics(client: AsyncClient) -> None:
    created = (await client.post("/analyses", json={"text": "delete me"})).json()
    assert (await client.delete(f"/analyses/{created['id']}")).status_code == 204
    assert (await client.get(f"/analyses/{created['id']}")).status_code == 404


async def test_delete_missing_returns_404(client: AsyncClient) -> None:
    assert (await client.delete(f"/analyses/{uuid.uuid4()}")).status_code == 404