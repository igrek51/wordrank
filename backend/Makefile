.PHONY: deploy build run setup test

setup:
	pip install -r requirements.txt
	python setup.py develop

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yaml build

run-docker: build
	echo "Working on local modifiable copy"
	mkdir -p volumes
	cp -r db volumes/

	docker-compose up wordrank
	docker-compose rm -f wordrank

run-django:
	python -u wordrank/djangoapp/manage.py runserver 0.0.0.0:8000 --noreload

run-fastapi:
	python -u wordrank/main.py

run: run-fastapi

recreate-db:
	rm -f db/wordrank.sqlite
	python wordrank/djangoapp/manage.py makemigrations words
	python wordrank/djangoapp/manage.py migrate
	python wordrank/djangoapp/manage.py createsuperuser

add-migration:
	python wordrank/djangoapp/manage.py makemigrations words
	python wordrank/djangoapp/manage.py migrate
