FROM jenkins/jenkins:lts-jdk11

RUN mkdir /var/jenkins_home/.ssh && ssh-keyscan -t rsa github.com >> /var/jenkins_home/.ssh/known_hosts

USER root

RUN apt-get update && apt-get install -y make gcc python3.9

RUN curl https://get.docker.com/ | sh

RUN groupadd docker-in-docker --gid 1001 \
    && usermod -aG 1001 jenkins

USER jenkins

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

COPY ./plugins.txt /usr/share/jenkins/ref/plugins.txt

COPY ./job_dsl.groovy /usr/share/jenkins/ref/

RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

COPY . jenkins/

ENV CASC_JENKINS_CONFIG jenkins/jenkins-casc.yml