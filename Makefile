DOCKER_IMAGE := ninjadroid
DOCKER_TAG := latest
PWD := $(shell pwd)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod 755 ninjadroid/dex2jar/d2j-dex2jar.sh
	@pip3 install -r requirements.txt
	sudo ln -s $(ROOT_DIR)/ninjadroid.py /usr/local/bin/ninjadroid

build-macos:
	make build
	mv -f ninjadroid/aapt/aapt_macos ninjadroid/aapt/aapt

build-linux:
	make build
	mv -f ninjadroid/aapt/aapt_linux ninjadroid/aapt/aapt

.PHONY: build-docker
build-docker:
	@docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .


# Run:
.PHONY: run
run:
	@python3 ninjadroid.py $(apk)

.PHONY: run-docker
run-docker:
	@docker run -it --rm -v ${PWD}/apks:/apks ${DOCKER_IMAGE}:${DOCKER_TAG} json $(apk)

.PHONY: run-docker-with-output
run-docker-with-output:
	@docker run --rm -v ${PWD}/apks:/apks -v ${PWD}/output:/output ${DOCKER_IMAGE}:${DOCKER_TAG} ninjadroid -e /output $(apk)


# Test:
.PHONY: test
test:
	@python3 -m unittest -v tests.test

.PHONY: test-docker
test-docker:
	@docker run --rm -w /opt/NinjaDroid ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest -v tests.test

.PHONY: test-docker-with-reload
test-docker-with-reload:
	@docker run --rm -it -w /opt/NinjaDroid \
	-v ${PWD}/ninjadroid/parsers:/opt/NinjaDroid/ninjadroid/parsers \
	-v ${PWD}/tests:/opt/NinjaDroid/tests \
	${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest -v tests.test
