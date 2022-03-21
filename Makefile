.PHONY: deploy build run setup test

setup:
	python3.8 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	(cd backend && make setup)
	@echo Activate your venv: . venv/bin/activate

run-local:
	(cd backend && make run-fastapi)

run-docker:
	(cd backend && make run-docker)

run: run-local


build-backend:
	(cd backend && make build)

build-frontend:
	cd frontend && \
	DOCKER_BUILDKIT=1 docker build -t webdict-frontend:latest -f Dockerfile .

build-frontend-replace: build-frontend
	set -e ;\
	rm -rf backend/static/* ;\
	ID=$$(docker create webdict-frontend:latest) ;\
	echo $$ID ;\
	docker cp "$$ID:/build/static" backend/ ;\
	docker rm -v $$ID ;\

build: build-backend


deploy: build-backend
	cd deploy && \
	ansible-playbook -i inventory.yaml deploy-playbook.yaml

deploy-copy-volumes: build-backend
	cd deploy && \
	ansible-playbook -i inventory.yaml deploy-playbook.yaml --extra-vars "copy_volumes=true"
