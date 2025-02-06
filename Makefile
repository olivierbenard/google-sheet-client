.PHONY: tests test-coverage

run:
	poetry run python google_sheet_client/client.py

black:
	poetry run black .

mypy:
	poetry run mypy google_sheet_client/

pylint:
	poetry run pylint google_sheet_client/

tests:
	poetry run pytest -vvs tests/

test-coverage:
	poetry run pytest --cov=google_sheet_client --cov-branch --cov-report=term-missing --cov-fail-under=90

checks: black mypy pylint tests test-coverage

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
