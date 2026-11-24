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

restorecsv:
	docker compose down -v 
	docker compose up -d
	docker exec -it vitalx_db psql -U postgres -c "DROP DATABASE vitalx;"
	docker exec -it vitalx_db psql -U postgres -c "CREATE DATABASE vitalx;"
	docker exec -it vitalx_app uv run python -c "from vitalx.dbutils import create_schemas; create_schemas()"
	docker exec -it vitalx_app uv run python -m src.vitalx.csv_backup

restorepgmac:
	docker compose down -v 
	docker compose up -d
	docker exec -it vitalx_db psql -U postgres -c "DROP DATABASE vitalx;"
	docker exec -it vitalx_db psql -U postgres -c "CREATE DATABASE vitalx;"
	docker exec -it vitalx_app uv run python -c "from vitalx.dbutils import create_schemas; create_schemas()"
	gunzip < backups/vitalx_backup_yyyy-mm-dd.sql.gz | docker exec -i vitalx_db psql -U postgres -d vitalx

verify:
	docker exec -it vitalx_db psql -U postgres -d vitalx -c "SELECT 'vitalx_walk' AS table_name, COUNT(*) FROM vitalx_walk UNION ALL SELECT 'vitalx_sleep', COUNT(*) FROM vitalx_sleep UNION ALL SELECT 'vitalx_streak', COUNT(*) FROM vitalx_streak UNION ALL SELECT 'weather', COUNT(*) FROM weather;" 
