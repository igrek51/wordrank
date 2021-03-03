.PHONY: deploy build run setup test

setup:
	pip install -r requirements.txt
	python setup.py develop

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yaml build

run-docker: build
	docker run --rm -it -p 8000:8000 webdict

run-django:
	python -u webdict/djangoapp/manage.py runserver 0.0.0.0:8000 --noreload

run-fastapi:
	python -u webdict/main.py

run: run-fastapi

recreate-db:
	rm -f db/webdict.sqlite
	python webdict/djangoapp/manage.py makemigrations words
	python webdict/djangoapp/manage.py migrate
	python webdict/djangoapp/manage.py createsuperuser
