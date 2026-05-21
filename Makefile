.PHONY: test lint type cov complexity all

test:
	pytest -v

cov:
	pytest --cov=. --cov-report=term-missing --cov-report=html

lint:
	python3 -m ruff check .

type:
	python3 -m mypy --strict src legacy.py

complexity:
	python3 -m radon cc src legacy.py -s -a

all: lint type test cov complexity
