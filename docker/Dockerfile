FROM openjdk:21-slim-bookworm

ENV NINJADROID_HOME=/opt/NinjaDroid
ENV NINJADROID_USER=ninjadroid

ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_TOOLS_VERSION=25.2.5
ENV ANDROID_SDK_API_LEVELS=android-29
ENV ANDROID_SDK_BUILD_TOOLS_VERSION=29.0.3
ENV ANDROID_SDK_EXTRAS=""

# Install general dependencies

RUN apt update \
    && apt install -qy python3 pipenv unzip wget binutils

# Install Android SDK

ENV PATH=${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/tools/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/build-tools/${ANDROID_SDK_BUILD_TOOLS_VERSION}

RUN mkdir -p /opt/android-sdk && cd /opt \
    && wget -q http://dl.google.com/android/repository/tools_r${ANDROID_SDK_TOOLS_VERSION}-linux.zip -O android-sdk-tools.zip \
    && unzip -q android-sdk-tools.zip -d ${ANDROID_HOME} \
    && rm -f android-sdk-tools.zip \
    && echo y | android update sdk --no-ui -a --filter tools,platform-tools,${ANDROID_SDK_EXTRAS},${ANDROID_SDK_API_LEVELS},build-tools-${ANDROID_SDK_BUILD_TOOLS_VERSION} --no-https

# Install NinjaDroid

RUN useradd -ms /bin/bash ${NINJADROID_USER} && \
    mkdir -p ${NINJADROID_HOME}

COPY Pipfile ${NINJADROID_HOME}/Pipfile
COPY Pipfile.lock ${NINJADROID_HOME}/Pipfile.lock
COPY ninjadroid.py ${NINJADROID_HOME}
COPY ninjadroid/ ${NINJADROID_HOME}/ninjadroid/

# NOTE: To install only production dependencies remove the "--dev" flag from the below "pipenv install" command!
#RUN PIPENV_PIPFILE=${NINJADROID_HOME}/Pipfile pipenv install --system --deploy \
RUN PIPENV_PIPFILE=${NINJADROID_HOME}/Pipfile pipenv install --dev --system --deploy \
    && ln -s ${ANDROID_HOME}/build-tools/${ANDROID_SDK_BUILD_TOOLS_VERSION}/aapt ${NINJADROID_HOME}/ninjadroid/aapt/aapt \
    && chmod a+x ${NINJADROID_HOME}/ninjadroid/aapt/aapt \
    && chmod a+x ${NINJADROID_HOME}/ninjadroid/apktool/apktool.jar \
    && chmod -R a+x ${NINJADROID_HOME}/ninjadroid/dex2jar/ \
    && mkdir -p /var/log/ninjadroid \
    && chgrp -R ninjadroid /var/log/ninjadroid \
    && chmod -R g+w /var/log/ninjadroid \
    && ln -s ${NINJADROID_HOME}/ninjadroid.py /usr/local/bin/ninjadroid

USER ninjadroid
WORKDIR /home/ninjadroid

# Run NinjaDroid

CMD ["ninjadroid", "-h"]
