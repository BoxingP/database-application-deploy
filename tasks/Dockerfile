FROM openjdk:8-jdk-alpine
RUN apk add --no-cache curl tar bash
ARG MAVEN_MAJOR=3
ARG MAVEN_VERSION=3.8.1
ARG MAVEN_FILE=apache-maven-${MAVEN_VERSION}-bin.tar.gz
ARG BASE_URL=https://downloads.apache.org/maven/maven-${MAVEN_MAJOR}/${MAVEN_VERSION}/binaries
ARG USER_HOME_DIR="/root"
RUN mkdir -p /usr/share/maven && curl -fsSL -o /tmp/apache-maven.tar.gz $BASE_URL/$MAVEN_FILE && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 && rm -f /tmp/apache-maven.tar.gz && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn
ENV MAVEN_HOME=/usr/share/maven
ENV MAVEN_CONFIG="${USER_HOME_DIR}/.m2"
ENV MAVEN_OPTS="-XX:+TieredCompilation -XX:TieredStopAtLevel=1"