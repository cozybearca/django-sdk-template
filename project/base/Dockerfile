FROM ubuntu:20.04@sha256:d5a6519d9f048100123c568eb83f7ef5bfcad69b01424f420f17c932b00dea76

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing
RUN apt-get install -y curl ca-certificates gnupg

RUN apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get install -y tzdata
ENV TZ America/Toronto

RUN apt-get install -y sudo
RUN apt-get install -y wait-for-it
RUN apt-get install -y python3.8 python3-pip git
RUN apt-get install -y openssl libssl-dev openssh-client openssh-server
RUN apt-get install -y postgresql-client-12
RUN python3.8 -m pip install click debugpy
RUN apt-get install -y iputils-ping iproute2 dnsutils

RUN echo 'ALL ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
