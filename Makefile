# tests:
# 	python -m unittest discover tests

run:
	python -m sandbox

lint:
	python -m pylint game_engine

lint_fast:
	python -m flake8 game_engine

type_check:
	python -m mypy game_engine --ignore-missing-imports

install:
	pip install -r requirements.txt

.PHONY: run tests
