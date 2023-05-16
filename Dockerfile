FROM ghcr.io/penguincloud/core:main
LABEL company="Penguin Tech Group LLC"
LABEL org.opencontainers.image.authors="info@penguintech.group"
LABEL license="GNU AGPL3"

# GET THE FILES WHERE WE NEED THEM!
COPY . /opt/manager/
WORKDIR /opt/manager

RUN apt update && apt upgrade -y
# PUT YER ARGS in here
ARG APP_TITLE="PTGAPP" # Change this to actual title for Default
ARG BUILD_THREADS="4"
ARG IPERF_URL="https://github.com/esnet/iperf/archive/refs/tags/3.13.tar.gz"

# BUILD IT!
RUN ansible-playbook build.yml -c local

# Environment variables
ENV IPERF_SERVER_ENABLE="1"
ENV IPERF_SERVER_IP="127.0.0.1"
ENV IPERF_SERVER_PORT="5201"
ENV IPERF_CLIENT_STREAMS="5"
ENV IPERF_FORMAT="default"
ENV IPERF3_PASSWORD="changeme"
ENV IPERF_USERNAME="ptg-user"
ENV IPERF_PROTOCOL="TCP"
ENV WEB_PORT="8080"

# Switch to non-root user
USER ptg-user

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
