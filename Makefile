.PHONY: help install run test clean migrate

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run development server"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean cache files"
	@echo "  make lint       - Run linting"

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
