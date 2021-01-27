FROM ubuntu:20.04@sha256:d5a6519d9f048100123c568eb83f7ef5bfcad69b01424f420f17c932b00dea76

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing
RUN apt-get install -y sudo
# install docker dependencies
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
# install other tools
RUN apt-get install -y man && yes | unminimize
RUN apt-get install -y git git-lfs
RUN apt-get install -y python3.8 python3-pip
RUN apt-get install -y wait-for-it
RUN apt-get install -y certbot
# optional debug tools
RUN apt-get install -y iputils-ping iproute2 dnsutils
RUN apt-get install -y vim
# install nodejs, yarn
RUN (curl -sL https://deb.nodesource.com/setup_12.x | bash -) && \
    (curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -) && \
    (echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list) && \
    (apt-get update && apt-get install -y yarn)

# install docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && apt-get install -y \
    docker-ce docker-ce-cli containerd.io && \
    curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose


RUN python3.8 -m pip install flake8 bandit autopep8 pylint black rope
RUN npm install --global prettier yo vsce

RUN adduser --home /home/sdk --shell /bin/bash --gecos "" --disabled-password --ingroup docker sdk
RUN echo 'sdk ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

ARG PROJ_NAME
ARG HOST_PORT_SPACE

COPY sdk/bin /opt/bin
ENV PATH /opt/bin:$PATH

ENV PROJ_NAME ${PROJ_NAME}
ENV HOST_PORT_SPACE ${HOST_PORT_SPACE}
ENV SDK_ROOT /${PROJ_NAME}-sdk
ENV SDK_PROJECT_DIR ${SDK_ROOT}/project
ENV PYTHONPATH ${SDK_ROOT}/sdk:${SDK_PROJECT_DIR}/site:${SDK_PROJECT_DIR}/site/deps
ENV IMAGE_PREFIX docker.pkg.github.com/cozybearca/${PROJ_NAME}/
ENV NODE_PATH ${SDK_PROJECT_DIR}/site/tests/node_modules:${SDK_PROJECT_DIR}/site/src/web/node_modules:${SDK_PROJECT_DIR}/site/src
ENV PATH ${SDK_PROJECT_DIR}/site/tests/node_modules/.bin:${SDK_PROJECT_DIR}/site/src/web/node_modules/.bin:${PATH}
ENV DJANGO_SETTINGS_MODULE src.settings
ENV SITE_ROOT ${SDK_PROJECT_DIR}/site
ENV MIGRATION_DIR ${SDK_PROJECT_DIR}/site/migrations
ENV COLLECT_STATIC_DIR ${SDK_PROJECT_DIR}/site/collectstatic

RUN mkdir -p ${SDK_PROJECT_DIR}
WORKDIR ${SDK_PROJECT_DIR}

CMD [ "/opt/bin/entrypoint" ]
