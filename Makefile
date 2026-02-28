.PHONY: help install run test clean migrate migrate-create migrate-up migrate-down migrate-history migrate-current

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make run              - Run development server"
	@echo "  make test             - Run tests"
	@echo "  make clean            - Clean cache files"
	@echo "  make lint             - Run linting"
	@echo ""
	@echo "Database Migrations:"
	@echo "  make migrate-create   - Create new migration (auto-generate from models)"
	@echo "  make migrate-up       - Apply all pending migrations"
	@echo "  make migrate-down     - Rollback last migration"
	@echo "  make migrate-history  - Show migration history"
	@echo "  make migrate-current  - Show current migration status"

install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

test:
	pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

lint:
	flake8 app/
	mypy app/

format:
	black app/
	isort app/

docker-build:
	docker build -t fastapi-ordering .

docker-run:
	docker run -p 8000:8000 fastapi-ordering

# Database Migrations
migrate-create:
	@read -p "Enter migration message: " msg; \
	../venv/bin/alembic revision --autogenerate -m "$$msg"

migrate-up:
	../venv/bin/alembic upgrade head

migrate-down:
	../venv/bin/alembic downgrade -1

migrate-history:
	../venv/bin/alembic history --verbose

migrate-current:
	../venv/bin/alembic current

migrate-show:
	@echo "Current database status:"
	@../venv/bin/alembic current
	@echo ""
	@echo "Recent migrations:"
	@../venv/bin/alembic history -r-3:
