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
	@pip3 install -r requirements.txt

build-macos:
	#make build
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod -R 755 ninjadroid/dex2jar/
	@pip3 install coverage==5.5
	@pip3 install parameterized==0.8.1
	@pip3 install pylint==2.6.2
	@pip3 install python-dateutil==2.8.1
	@pip3 install typing==3.7.4
	@pip3 install tzlocal==2.1
	@pip3 install pyaxmlparser==0.3.24 --user
	mv -f ninjadroid/aapt/aapt_macos ninjadroid/aapt/aapt

build-linux:
	make build
	mv -f ninjadroid/aapt/aapt_linux ninjadroid/aapt/aapt

.PHONY: build-docker
build-docker:
	@docker build -f ${DOCKER_FILE} -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

.PHONY: build-flatpak
build-flatpak:
	@flatpak install flathub org.freedesktop.Platform//20.08 org.freedesktop.Sdk//20.08 --user
	@flatpak install flathub org.freedesktop.Sdk.Extension.openjdk11//20.08 --user
	@flatpak install flathub org.freedesktop.Sdk.Extension.toolchain-i386//20.08 --user
	@flatpak-builder flatpak/build ${FLATPAK_MANIFEST} --force-clean

.PHONY: build-snap
build-snap:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -f ninjadroid_*.snap
	@snapcraft clean
	@snapcraft


# Install:
.PHONY: install
install:
	sudo ln -s $(NINJADROID_HOME)/ninjadroid.py /usr/local/bin/ninjadroid

.PHONY: uninstall
uninstall:
	sudo unlink /usr/local/bin/ninjadroid

.PHONY: install-snap
install-snap:
	snap install ninjadroid_4.5_amd64.snap --devmode

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
	@python3 ninjadroid.py $(apk)

.PHONY: run-docker
run-docker:
	@docker run --name ${DOCKER_IMAGE} -it --rm -v ${PWD}/apks:/apks ${DOCKER_IMAGE}:${DOCKER_TAG} ninjadroid $(apk)

.PHONY: run-flatpak
run-flatpak:
	@flatpak-builder --run flatpak/build ${FLATPAK_MANIFEST} ninjadroid $(apk)


# Test:
.PHONY: test
test:
	@python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@coverage3 run --source=. --omit="tests/*,regression/*" -m unittest
	@coverage3 report

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaDroid -v ${NINJADROID_HOME}/tests:/opt/NinjaDroid/tests ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest

.PHONY: regression
regression:
	@python3 regression/native.py

.PHONY: regression-docker
regression-docker:
	@python3 regression/docker.py

.PHONY: regression-flatpak
regression-flatpak:
	@python3 regression/flatpak.py

.PHONY: regression-snap
regression-snap:
	@python3 regression/snap.py

.PHONY: checkstyle
checkstyle:
	pylint ninjadroid.py ninjadroid/ tests/ regression/

.PHONY: checkstyle-docker
checkstyle-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/NinjaDroid -v ${NINJADROID_HOME}/.pylintrc:/opt/NinjaDroid/.pylintrc -v ${NINJADROID_HOME}/tests:/opt/NinjaDroid/tests -v ${NINJADROID_HOME}/regression:/opt/NinjaDroid/regression ${DOCKER_IMAGE}:${DOCKER_TAG} pylint ninjadroid.py ninjadroid/ tests/ regression/
