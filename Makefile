test:
	pytest -v

cov:
	pytest --cov=. --cov-report=term-missing --cov-report=html

all: test cov