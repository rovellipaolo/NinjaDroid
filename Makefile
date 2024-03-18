DOCKER_FILE :=  docker/Dockerfile
DOCKER_IMAGE := ninjadroid
DOCKER_TAG := latest
FLATPAK_MANIFEST := flatpak/com.github.rovellipaolo.NinjaDroid.yaml
PWD := $(shell pwd)
NINJADROID_HOME := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod -R 755 ninjadroid/dex2jar/
	@which pipenv || pip3 install pipenv
	@pipenv install --dev

build-macos:
	make build
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod -R 755 ninjadroid/dex2jar/
	mv -f ninjadroid/aapt/aapt_macos ninjadroid/aapt/aapt

build-linux:
	make build
	mv -f ninjadroid/aapt/aapt_linux ninjadroid/aapt/aapt

.PHONY: build-docker
build-docker:
	@docker build -f ${DOCKER_FILE} -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

.PHONY: build-flatpak
build-flatpak:
	@flatpak install flathub org.freedesktop.Platform//22.08 org.freedesktop.Sdk//22.08 --user
	@flatpak install flathub org.freedesktop.Sdk.Extension.openjdk21//22.08 --user
	@flatpak install flathub org.freedesktop.Sdk.Extension.toolchain-i386//22.08 --user
	@flatpak-builder flatpak/build ${FLATPAK_MANIFEST} --force-clean

.PHONY: build-snap
build-snap:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -f ninjadroid_*.snap
	@snapcraft clean
	@snapcraft

.PHONY: generate-checkstyle-config
generate-checkstyle-config:
	pylint --generate-rcfile > .pylintrc


# Install:
.PHONY: install
install:
	sudo ln -s ${NINJADROID_HOME}/ninjadroid.py /usr/local/bin/ninjadroid

.PHONY: uninstall
uninstall:
	sudo unlink /usr/local/bin/ninjadroid

.PHONY: install-snap
install-snap:
	snap install ninjadroid_4.5.1_amd64.snap --devmode

.PHONY: uninstall-snap
uninstall-snap:
	snap remove ninjadroid

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
	@pipenv run python3 ninjadroid.py $(apk)

.PHONY: run-docker
run-docker:
	@docker run --name ${DOCKER_IMAGE} -it --rm -v ${PWD}/apks:/apks ${DOCKER_IMAGE}:${DOCKER_TAG} ninjadroid $(apk)

.PHONY: run-flatpak
run-flatpak:
	@flatpak-builder --run flatpak/build ${FLATPAK_MANIFEST} ninjadroid $(apk)


# Test:
.PHONY: test
test:
	@pipenv run python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@pipenv run coverage3 run --source=. --omit="tests/*,regression/*" -m unittest
	@pipenv run coverage3 report

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaDroid -v ${NINJADROID_HOME}/tests:/opt/NinjaDroid/tests ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest

.PHONY: regression
regression:
	@pipenv run python3 regression/native.py

.PHONY: regression-docker
regression-docker:
	@pipenv run python3 regression/docker.py

.PHONY: regression-flatpak
regression-flatpak:
	@pipenv run python3 regression/flatpak.py

.PHONY: regression-snap
regression-snap:
	@pipenv run python3 regression/snap.py

.PHONY: checkstyle
checkstyle:
	@pipenv run pycodestyle --max-line-length=120 ninjadroid.py ninjadroid/ tests/ regression/
	@pipenv run pylint ninjadroid.py ninjadroid/ tests/ regression/

.PHONY: checkstyle-docker
checkstyle-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaDroid -v ${NINJADROID_HOME}/.pylintrc:/opt/NinjaDroid/.pylintrc -v ${NINJADROID_HOME}/tests:/opt/NinjaDroid/tests -v ${NINJADROID_HOME}/regression:/opt/NinjaDroid/regression ${DOCKER_IMAGE}:${DOCKER_TAG} pycodestyle --max-line-length=120 ninjadroid.py ninjadroid/ tests/ regression/ && pylint ninjadroid.py ninjadroid/ tests/ regression/
