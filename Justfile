set shell := ["bash", "-lc"]

venv := ".venv"

@default:
    just --list

install:
    uv venv {{venv}}
    source {{venv}}/bin/activate && uv sync --extra tests

install-tests: install

mypy:
    source {{venv}}/bin/activate && mypy .

test:
    source {{venv}}/bin/activate && pytest

test-unit:
    source {{venv}}/bin/activate && pytest tests/test_client_unit.py

test-integration:
    source {{venv}}/bin/activate && pytest -m integration
