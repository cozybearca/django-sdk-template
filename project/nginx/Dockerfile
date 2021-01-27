ARG TAG
ARG IMAGE_PREFIX
ARG PROJ_NAME
FROM ${IMAGE_PREFIX}${PROJ_NAME}-base:${TAG}

RUN apt-get install -y nginx

COPY conf.d /etc/nginx/conf.d
# add dummy certs so nginx doesn't shutdown
COPY cert/bad /cert
CMD nginx -g "daemon off;"
