test:
    uv run pytest ./tests

coverage:
    uv run coverage run -m pytest ./tests && uv run coverage report -m

format:
    uv run ruff format . && uv run ruff check --fix .