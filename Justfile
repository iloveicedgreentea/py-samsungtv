set shell := ["bash", "-lc"]

venv := ".venv"

@default:
    just --list

install:
    uv venv {{venv}}
    source {{venv}}/bin/activate && uv pip install -e .

install-tests: install
    source {{venv}}/bin/activate && uv pip install -e .[tests]

mypy:
    source {{venv}}/bin/activate && mypy .

test:
    source {{venv}}/bin/activate && pytest

test-unit:
    source {{venv}}/bin/activate && pytest tests/test_client_unit.py

test-integration:
    source {{venv}}/bin/activate && pytest -m integration
