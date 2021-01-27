ARG TAG
ARG IMAGE_PREFIX
ARG PROJ_NAME
FROM ${IMAGE_PREFIX}${PROJ_NAME}-base:${TAG}

# Base settings
ENV HOME /root
ENV SITE_ROOT /site
ENV PATH ${SITE_ROOT}/bin:${PATH}
ENV MIGRATION_DIR ${SITE_ROOT}/migrations
ENV PYTHONSTARTUP ${SITE_ROOT}/.startup.py
ENV DJANGO_SETTINGS_MODULE src.settings
ENV COLLECT_STATIC_DIR ${SITE_ROOT}/collectstatic
ENV PYTHONPATH ${SITE_ROOT}:${SITE_ROOT}/deps

COPY .ipython_config.py ${HOME}/.ipython/profile_default/ipython_config.py
COPY . ${SITE_ROOT}
# uwsgi dependencies
RUN apt-get install -y libpcre3 libpcre3-dev
RUN pip3 install -r ${SITE_ROOT}/requirements.txt

CMD entrypoint
