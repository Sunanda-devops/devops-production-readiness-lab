.PHONY: install test lint security check docker-build

install:
	python -m pip install -r requirements-dev.txt

test:
	pytest -q

lint:
	ruff check .

security:
	bandit -r app -ll

docker-build:
	docker build --tag production-readiness-api:local .

check: test lint security
