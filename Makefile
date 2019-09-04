IMAGE := ninjadroid

.PHONY: default
default: build

.PHONY: build
build:
	@docker build \
		--pull \
		--tag ${IMAGE}:latest \
		.
