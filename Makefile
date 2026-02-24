.PHONY: help install dev test lint format clean build

help:
	@echo "Available commands:"
	@echo "  install       - install package"
	@echo "  dev           - install in development mode"
	@echo "  test          - run tests"
	@echo "  lint          - run linters"
	@echo "  format        - format code"
	@echo "  clean         - clean build artifacts"
	@echo "  build         - build distribution packages"

install:
	pip install .

dev:
	pip install -e .

test:
	pytest tests/ -v --cov=anytype

lint:
	ruff check anytype/
	mypy anytype/

format:
	black anytype/ tests/
	isort anytype/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build
