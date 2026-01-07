format:
    uv run ruff format . && uv run ruff check --fix .

dev:
    uv run fastapi dev main.py

run:
    uv run fastapi run main.py

test:
    uv run pytest tests/

coverage:
    uv run coverage run -m pytest tests/ && uv run coverage report -m

snapshot:
    uv run fastapi dev tests/snapshot/app.py