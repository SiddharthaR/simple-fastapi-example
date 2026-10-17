import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def clear_items():
    main.items.clear()
    yield
    main.items.clear()


@pytest.fixture
def client():
    return TestClient(main.app)
