import pytest


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_item(client):
    response = client.post("/items", json={"text": "apple"})

    assert response.status_code == 200
    assert response.json() == [{"text": "apple", "is_done": False}]


def test_create_item_with_is_done(client):
    response = client.post("/items", json={"text": "apple", "is_done": True})

    assert response.status_code == 200
    assert response.json() == [{"text": "apple", "is_done": True}]


def test_create_item_with_empty_body_uses_defaults(client):
    response = client.post("/items", json={})

    assert response.status_code == 200
    assert response.json() == [{"text": None, "is_done": False}]


def test_create_item_returns_all_items(client):
    client.post("/items", json={"text": "apple"})
    response = client.post("/items", json={"text": "banana"})

    assert [item["text"] for item in response.json()] == ["apple", "banana"]


@pytest.mark.parametrize(
    "payload",
    [
        {"text": ["not", "a", "string"]},
        {"text": "apple", "is_done": "not-a-bool"},
    ],
)
def test_create_item_invalid_payload_returns_422(client, payload):
    response = client.post("/items", json=payload)

    assert response.status_code == 422


def test_create_item_missing_body_returns_422(client):
    response = client.post("/items")

    assert response.status_code == 422


def test_list_items_empty(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_list_items_default_limit_is_10(client):
    for i in range(12):
        client.post("/items", json={"text": f"item {i}"})

    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 10


def test_list_items_with_limit(client):
    for i in range(5):
        client.post("/items", json={"text": f"item {i}"})

    response = client.get("/items", params={"limit": 2})

    assert response.status_code == 200
    assert response.json() == [
        {"text": "item 0", "is_done": False},
        {"text": "item 1", "is_done": False},
    ]


def test_list_items_invalid_limit_returns_422(client):
    response = client.get("/items", params={"limit": "abc"})

    assert response.status_code == 422


def test_get_item(client):
    client.post("/items", json={"text": "apple"})
    client.post("/items", json={"text": "banana", "is_done": True})

    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json() == {"text": "banana", "is_done": True}


def test_get_item_not_found_returns_404(client):
    client.post("/items", json={"text": "apple"})

    response = client.get("/items/5")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item 5 not found"}


def test_get_item_non_integer_id_returns_422(client):
    response = client.get("/items/abc")

    assert response.status_code == 422


def test_get_item_negative_id_returns_404(client):
    client.post("/items", json={"text": "apple"})

    response = client.get("/items/-1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item -1 not found"}


def test_get_item_negative_id_on_empty_list_returns_404(client):
    response = client.get("/items/-1")

    assert response.status_code == 404
