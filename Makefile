format:
	uv run ruff format .

lint:
	uv run ruff check --fix .

typecheck:
	uv run ty check

check: format lint typecheck

build:
	uv build

prep:
	prek run --all-files
