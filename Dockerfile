FROM ghcr.io/penguincloud/core:v5.0.1
LABEL company="Penguin Tech Group LLC"
LABEL org.opencontainers.image.authors="info@penguintech.group"
LABEL license="GNU AGPL3"

# GET THE FILES WHERE WE NEED THEM!
COPY . /opt/manager/
WORKDIR /opt/manager


# PUT YER ARGS in here
ARG APP_TITLE="PTGAPP" # Change this to actual title for Default
ARG BUILD_THREADS="4"
ARG IPERF_URL="https://github.com/esnet/iperf/archive/refs/tags/3.13.tar.gz"

# BUILD IT!
RUN ansible-playbook build.yml -c local

# PUT YER ENVS in here
ENV HELLO="WORLD"

# Switch to non-root user
USER ptg-user

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
