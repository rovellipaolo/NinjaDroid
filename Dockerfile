FROM openjdk:8u212-jre-slim-stretch

ENV NINJADROID_DIR=/opt/NinjaDroid
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_TOOLS_VERSION=25.2.5
ENV ANDROID_SDK_API_LEVELS=android-23
ENV ANDROID_SDK_BUILD_TOOLS_VERSION=25.0.2
ENV ANDROID_SDK_EXTRAS=""
ENV PATH=${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/tools/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/build-tools/${ANDROID_SDK_BUILD_TOOLS_VERSION}

RUN useradd -ms /bin/bash ninjadroid

# Install dependencies
RUN apt update && \
    apt install -qy git python3 python3-pip unzip wget binutils libstdc++

# Install Android SDK
RUN mkdir -p /opt/android-sdk && cd /opt \
    && wget -q http://dl.google.com/android/repository/tools_r${ANDROID_SDK_TOOLS_VERSION}-linux.zip -O android-sdk-tools.zip \
    && unzip -q android-sdk-tools.zip -d ${ANDROID_HOME} \
    && rm -f android-sdk-tools.zip \
    && echo y | android update sdk --no-ui -a --filter tools,platform-tools,${ANDROID_SDK_EXTRAS},${ANDROID_SDK_API_LEVELS},build-tools-${ANDROID_SDK_BUILD_TOOLS_VERSION} --no-https

# Install NinjaDroid
RUN mkdir -p ${NINJADROID_DIR}
COPY requirements.txt ${NINJADROID_DIR}
COPY ninjadroid.py ${NINJADROID_DIR}
COPY ninjadroid/ ${NINJADROID_DIR}/ninjadroid/
COPY tests/ ${NINJADROID_DIR}/tests/

RUN pip3 install -r ${NINJADROID_DIR}/requirements.txt \
    && ln -s ${ANDROID_HOME}/build-tools/${ANDROID_SDK_BUILD_TOOLS_VERSION}/aapt ${NINJADROID_DIR}/ninjadroid/aapt/aapt \
    && chmod a+x ${NINJADROID_DIR}/ninjadroid/aapt/aapt \
    && chmod a+x ${NINJADROID_DIR}/ninjadroid/apktool/apktool.jar \
    && chmod a+x ${NINJADROID_DIR}/ninjadroid/dex2jar/d2j-dex2jar.sh

RUN mkdir -p /var/log/ninjadroid \
    && chgrp -R ninjadroid /var/log/ninjadroid \
    && chmod -R g+w /var/log/ninjadroid

COPY ninjadroid.sh ${NINJADROID_DIR}

USER ninjadroid
WORKDIR /home/ninjadroid

# Run NinjaDroid
ENTRYPOINT ["/opt/NinjaDroid/ninjadroid.sh"]
CMD ["ninjadroid.py", "-h"]
