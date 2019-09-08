IMAGE := ninjadroid

.PHONY: default
default: build-docker

.PHONY: build-docker
build-docker:
	docker build -t ${IMAGE}:latest .

.PHONY: test-docker
test-docker:
	@docker run --rm \
		-w /opt/NinjaDroid \
		-v $$(pwd)/tests:/opt/NinjaDroid/tests \
		${IMAGE}:latest \
		python3 -m unittest -v tests.test
