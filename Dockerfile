#FROM openjdk:11.0.3-slim-stretch
FROM openjdk:8u212-jre-slim-stretch

ENV ANDROID_HOME=/opt/android-sdk-linux
ENV SDK_TOOLS_VERSION=25.2.5
ENV API_LEVELS=android-23
ENV BUILD_TOOLS_VERSION=25.0.2
ENV ANDROID_EXTRAS=""
ENV PATH=${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/tools/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/build-tools/${BUILD_TOOLS_VERSION}
ENV NINJADROID_DIR=/opt/NinjaDroid

RUN useradd -ms /bin/bash ninjadroid

RUN apt update && apt install -qy git python3 python3-pip unzip wget binutils libstdc++

# Install Android SDK
RUN mkdir -p /opt/android-sdk-linux && cd /opt \
        && wget -q http://dl.google.com/android/repository/tools_r${SDK_TOOLS_VERSION}-linux.zip -O android-sdk-tools.zip \
        && unzip -q android-sdk-tools.zip -d ${ANDROID_HOME} \
        && rm -f android-sdk-tools.zip \
        && echo y | android update sdk --no-ui -a --filter tools,platform-tools,${ANDROID_EXTRAS},${API_LEVELS},build-tools-${BUILD_TOOLS_VERSION} --no-https

# Copy over and configure NinjaDroid
RUN mkdir -p ${NINJADROID_DIR}

COPY requirements.txt ${NINJADROID_DIR}
RUN pip3 install -r ${NINJADROID_DIR}/requirements.txt

COPY ninjadroid.py ${NINJADROID_DIR}
COPY ninjadroid/ ${NINJADROID_DIR}/ninjadroid/
RUN rm ${NINJADROID_DIR}/ninjadroid/aapt/aapt \
        && ln -s ${ANDROID_HOME}/build-tools/${BUILD_TOOLS_VERSION}/aapt ${NINJADROID_DIR}/ninjadroid/aapt/aapt \
        && chmod a+x ${NINJADROID_DIR}/ninjadroid/apktool/apktool.jar \
        && chmod a+x ${NINJADROID_DIR}/ninjadroid/dex2jar/d2j-dex2jar.sh

COPY entrypoint.sh /entrypoint.sh

RUN mkdir -p /var/log/ninjadroid && chgrp -R ninjadroid /var/log/ninjadroid && chmod -R g+w /var/log/ninjadroid
USER ninjadroid
WORKDIR /home/ninjadroid

ENTRYPOINT ["/entrypoint.sh"]
CMD ["ninjadroid.py", "-h"] # set default arg for entrypoint
