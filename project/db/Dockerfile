ARG TAG
ARG IMAGE_PREFIX
ARG PROJ_NAME
FROM ${IMAGE_PREFIX}${PROJ_NAME}-base:${TAG} as build-jieba

WORKDIR /root

RUN apt-get install -y postgresql-12 postgresql-server-dev-12
RUN apt-get install -y build-essential git cmake
RUN git clone https://github.com/jaiminpan/pg_jieba && cd pg_jieba && \
    git submodule update --init --recursive && \
    mkdir build && cd build && \
    cmake -DPostgreSQL_TYPE_INCLUDE_DIR=/usr/include/postgresql/12/server .. && \
    make && make install

########################################################################

ARG TAG
ARG IMAGE_PREFIX
ARG PROJ_NAME
FROM ${IMAGE_PREFIX}${PROJ_NAME}-base:${TAG}

# install postgres 12
RUN apt-get install -y postgresql-12 postgresql-12-repmgr

# clean up
RUN apt-get autoremove && apt-get clean

# install config files
# must be placed outside the volumes
# place at /etc instead of /var/lib which will be mounted to host
COPY postgresql.conf /etc/postgresql/12/main/postgresql.conf
COPY pg_hba.conf /etc/postgresql/12/main/pg_hba.conf
COPY sshd_config /etc/ssh/sshd_config
COPY bin /opt/bin

# install extensions
COPY --from=build-jieba     /usr/lib/postgresql/12/lib/pg_jieba.so                  /usr/lib/postgresql/12/lib/pg_jieba.so
COPY --from=build-jieba     /usr/share/postgresql/12/extension/pg_jieba.control     /usr/share/postgresql/12/extension/pg_jieba.control
COPY --from=build-jieba     /usr/share/postgresql/12/extension/pg_jieba--1.1.1.sql  /usr/share/postgresql/12/extension/pg_jieba--1.1.1.sql
COPY --from=build-jieba     /usr/share/postgresql/12/tsearch_data/jieba_base.dict   /usr/share/postgresql/12/tsearch_data/jieba_base.dict
COPY --from=build-jieba     /usr/share/postgresql/12/tsearch_data/jieba_hmm.model   /usr/share/postgresql/12/tsearch_data/jieba_hmm.model
COPY --from=build-jieba     /usr/share/postgresql/12/tsearch_data/jieba_user.dict   /usr/share/postgresql/12/tsearch_data/jieba_user.dict
COPY --from=build-jieba     /usr/share/postgresql/12/tsearch_data/jieba.stop        /usr/share/postgresql/12/tsearch_data/jieba.stop
COPY --from=build-jieba     /usr/share/postgresql/12/tsearch_data/jieba.idf         /usr/share/postgresql/12/tsearch_data/jieba.idf

# create default volumes
RUN mkdir -p /pg_wal_archive
RUN mkdir -p /pg_logs
RUN mkdir -p /etc/repmgr

VOLUME /pg_logs
VOLUME /pg_wal_archive
VOLUME /var/lib/postgresql/12/main

# set postgres user permissions
RUN usermod -aG sudo postgres
RUN passwd -d postgres
RUN echo 'postgres ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R postgres:postgres /etc/repmgr
RUN chown -R postgres:postgres /opt/bin && chmod u+x /opt/bin/*
RUN chown -R postgres:postgres /pg_wal_archive && chmod -R 0750 /pg_wal_archive
RUN chown -R postgres:postgres /etc/postgresql/12/main
RUN chown -R postgres:postgres /pg_logs

USER postgres

ENV PGDATA /var/lib/postgresql/12/main
ENV PATH /usr/lib/postgresql/12/bin/:$PATH
ENV PATH /opt/bin:$PATH

CMD entrypoint & sleep inf
