IMAGE := ninjadroid

.PHONY: default
default: build

.PHONY: build
build:
	@docker build \
		--pull \
		--tag ${IMAGE}:latest \
		.

.PHONY: docker-test
docker-test:
	@docker run --rm \
		-w /opt/NinjaDroid \
		-v $$(pwd)/tests:/opt/NinjaDroid/tests \
		${IMAGE}:latest \
		python3 -m unittest -v tests.test
