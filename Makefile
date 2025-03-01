.PHONY: setup test lint lint-fix clean build publish

setup:
	pip install uv
	uv venv
	uv pip install -e ".[dev]"

test:
	uvx nox -s pytest

lint:
	uvx nox -s lint

lint-fix:
	uvx nox -s lint_fix

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .hatch/

build:
	uv pip install build
	python -m build

publish:
	uv pip install twine
	python -m twine upload dist/*
