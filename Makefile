.PHONY: deploy build run setup test

setup:
	python3.8 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	pip install -r backend/requirements.txt
	@echo Activate your venv: . venv/bin/activate

build:
	cd backend && \
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yaml build

run: build
	docker run --rm -it -p 8011:8011 webdict
