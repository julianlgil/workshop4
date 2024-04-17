.PHONY:
	deps
	start
	install-pipenv

deps:
	python -m pipenv install --deploy

install-pipenv:
	python -m pip install "pipenv==2023.2.18"

APP_PORT ?= 8000
start:
	python -m pipenv run uvicorn main:app --reload --host 0.0.0.0 --port "$(APP_PORT)"
