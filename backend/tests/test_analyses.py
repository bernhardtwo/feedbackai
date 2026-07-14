"""Tests for the /analyses endpoints and the /health check."""
from uuid import uuid4

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_analysis_returns_201(client: TestClient) -> None:
    response = client.post("/analyses", json={"text": "This product is great"})

    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "This product is great"
    assert "id" in body
    assert "created_at" in body


def test_create_analysis_with_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/analyses", json={"text": ""})

    assert response.status_code == 422


def test_list_analyses_returns_all_created_items(client: TestClient) -> None:
    client.post("/analyses", json={"text": "first"})
    client.post("/analyses", json={"text": "second"})

    response = client.get("/analyses")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_analysis_returns_the_item(client: TestClient) -> None:
    created = client.post("/analyses", json={"text": "find me"}).json()

    response = client.get(f"/analyses/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_analysis_returns_404(client: TestClient) -> None:
    response = client.get(f"/analyses/{uuid4()}")

    assert response.status_code == 404


def test_delete_analysis_removes_it(client: TestClient) -> None:
    created = client.post("/analyses", json={"text": "delete me"}).json()

    delete_response = client.delete(f"/analyses/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/analyses/{created['id']}")
    assert get_response.status_code == 404


def test_delete_missing_analysis_returns_404(client: TestClient) -> None:
    response = client.delete(f"/analyses/{uuid4()}")

    assert response.status_code == 404