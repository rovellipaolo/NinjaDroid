DOCKER_IMAGE := ninjadroid
DOCKER_TAG := latest
PWD := $(shell pwd)
NINJADROID_HOME := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod -R 755 ninjadroid/dex2jar/
	@pip3 install -r requirements.txt

build-macos:
	#make build
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod -R 755 ninjadroid/dex2jar/
	@pip3 install coverage
	@pip3 install parameterized
	@pip3 install pylint
	@pip3 install python-dateutil
	@pip3 install typing
	@pip3 install tzlocal
	@pip3 install pyaxmlparser --user
	mv -f ninjadroid/aapt/aapt_macos ninjadroid/aapt/aapt

build-linux:
	make build
	mv -f ninjadroid/aapt/aapt_linux ninjadroid/aapt/aapt

.PHONY: build-docker
build-docker:
	@docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

.PHONY: build-flatpak
build-flatpak:
	@flatpak install flathub org.freedesktop.Platform//20.08 org.freedesktop.Sdk//20.08 --user
	@flatpak install flathub org.freedesktop.Sdk.Extension.openjdk11//20.08 --user
	@flatpak install flathub org.freedesktop.Sdk.Extension.toolchain-i386//20.08 --user
	@flatpak-builder flatpak/build flatpak/com.github.rovellipaolo.NinjaDroid.yaml --force-clean

# Install:
.PHONY: install
install:
	sudo ln -s $(NINJADROID_HOME)/ninjadroid.py /usr/local/bin/ninjadroid

.PHONY: uninstall
uninstall:
	sudo unlink /usr/local/bin/ninjadroid

.PHONY: install-githooks
install-githooks:
	@pip3 install pre-commit
	pre-commit install

.PHONY: uninstall-githooks
uninstall-githooks:
	pre-commit uninstall


# Run:
.PHONY: run
run:
	@python3 ninjadroid.py $(apk)

.PHONY: run-docker
run-docker:
	@docker run --name ${DOCKER_IMAGE} -it --rm -v ${PWD}/apks:/apks ${DOCKER_IMAGE}:${DOCKER_TAG} ninjadroid $(apk) --all --json

.PHONY: run-flatpak
run-flatpak:
	@flatpak-builder --run flatpak/build flatpak/com.github.rovellipaolo.NinjaDroid.yaml ninjadroid $(apk)


# Test:
.PHONY: test
test:
	@python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@coverage3 run --source=. -m unittest
	@coverage3 report

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaDroid -v ${NINJADROID_HOME}/tests:/opt/NinjaDroid/tests ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest

.PHONY: checkstyle
checkstyle:
	pylint ninjadroid.py ninjadroid/

.PHONY: checkstyle-docker
checkstyle-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaDroid -v ${NINJADROID_HOME}/.pylintrc:/opt/NinjaDroid/.pylintrc ${DOCKER_IMAGE}:${DOCKER_TAG} pylint ninjadroid.py ninjadroid/
