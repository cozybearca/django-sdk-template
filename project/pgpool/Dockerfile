ARG TAG
ARG IMAGE_PREFIX
ARG PROJ_NAME
FROM ${IMAGE_PREFIX}${PROJ_NAME}-base:${TAG}

# install postgres 12
RUN apt-get install -y pgpool2

# clean up
RUN apt-get autoremove && apt-get clean

COPY ssh_config /etc/ssh/ssh_config
COPY pgpool.live.conf /etc/pgpool2/pgpool.live.conf
COPY pgpool.dev.conf /etc/pgpool2/pgpool.dev.conf
COPY pcp.conf /etc/pgpool2/pcp.conf
COPY pcppass /etc/pgpool2/pcppass
COPY bin /opt/bin
COPY hooks /etc/pgpool2/hooks


# set postgres user permissions
RUN chown -R postgres:postgres /etc/pgpool2 && chmod u+x /etc/pgpool2/hooks/* && chmod 0600 /etc/pgpool2/pcppass
RUN chown -R postgres:postgres /opt/bin && chmod u+x /opt/bin/*

USER postgres

ENV PATH /opt/bin:$PATH
ENV PATH /usr/lib/postgresql/12/bin/:$PATH
ENV PCPPASSFILE /etc/pgpool2/pcppass

CMD ["entrypoint"]
