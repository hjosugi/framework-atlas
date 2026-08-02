from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_item() -> None:
    created = client.post("/items", json={"name": "book", "price": 12.5})
    assert created.status_code == 201
    item_id = created.json()["id"]

    fetched = client.get(f"/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "book"


def test_rejects_invalid_item() -> None:
    response = client.post("/items", json={"name": "", "price": -1})
    assert response.status_code == 422
    assert response.json() == {
        "code": "validation_error",
        "message": "request validation failed",
    }
