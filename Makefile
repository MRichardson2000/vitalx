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

test:
	uv run pytest

walkcheck:
	docker exec -it vitalx_db psql -U postgres -d vitalx -c "SELECT * FROM vitalx_walk;"

sleepcheck:
	docker exec -it vitalx_db psql -U postgres -d vitalx -c "SELECT * FROM vitalx_sleep;"

weather:
	docker exec -it vitalx_db psql -U postgres -d vitalx -c "SELECT * FROM weather;"