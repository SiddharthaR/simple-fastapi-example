# Simple FastAPI Example

This is a really basic example of a FastAPI application.

## Running the tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest --cov=main --cov-report=term-missing
```

- `tests/test_unit.py` calls the endpoint functions in `main.py` directly.
- `tests/test_integration.py` sends HTTP requests through FastAPI's `TestClient`.
