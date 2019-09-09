IMAGE := ninjadroid
PWD = $(shell pwd)


# Build:
.PHONY: build
build:
	sudo chmod 755 ninjadroid/aapt/aapt
	sudo chmod 755 ninjadroid/apktool/apktool.jar
	sudo chmod 755 ninjadroid/dex2jar/d2j-dex2jar.sh
	@pip3 install -r requirements.txt

build-macos:
	make build
	mv -f ninjadroid/aapt/aapt_macos ninjadroid/aapt/aapt

build-linux:
	make build
	mv -f ninjadroid/aapt/aapt_linux ninjadroid/aapt/aapt

.PHONY: build-docker
build-docker:
	@docker build -t ${IMAGE}:latest .


# Run:
.PHONY: run
run:
	@python ninjadroid.py $(APK)

.PHONY: run-docker
run-docker:
	@docker run -it --rm -v ${PWD}/apks:/apks ninjadroid:latest json $(APK)

.PHONY: run-docker-with-output
run-docker-with-output:
	@docker run --rm -v ${PWD}/apks:/apks -v $(pwd)/output:/output ninjadroid:latest ninjadroid -e /output $(APK)


# Test:
.PHONY: test
test:
	python -m unittest -v tests.test

.PHONY: test-docker
test-docker:
	@docker run --rm \
		-w /opt/NinjaDroid \
		-v $$(pwd)/tests:/opt/NinjaDroid/tests \
		${IMAGE}:latest \
		python3 -m unittest -v tests.test
