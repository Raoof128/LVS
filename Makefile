.PHONY: help install install-dev test lint format clean run

help:
	@echo "LLM Vulnerability Scanner - Makefile Commands"
	@echo "=============================================="
	@echo "install       - Install production dependencies"
	@echo "install-dev   - Install development dependencies"
	@echo "test          - Run test suite with coverage"
	@echo "lint          - Run linters (flake8, mypy)"
	@echo "format        - Format code with black and isort"
	@echo "clean         - Remove build artifacts and cache"
	@echo "run           - Start the application"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest -v --cov=backend --cov-report=term-missing --cov-report=html

lint:
	flake8 backend/ --max-line-length=100 --ignore=E203,W503
	mypy backend/ --ignore-missing-imports

format:
	black backend/ tests/
	isort backend/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

run:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
