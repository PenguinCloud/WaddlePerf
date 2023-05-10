FROM ubuntu:22.04 AS BUILD
ARG URL="https://github.com/esnet/iperf/archive/refs/tags/3.13.tar.gz"
COPY /bins/pre-build.sh /opt/pre-build.sh
WORKDIR /opt
RUN /opt/pre-build.sh

FROM ghcr.io/penguincloud/core:v5.0.1
LABEL company="Penguin Tech Group LLC"
LABEL org.opencontainers.image.authors="info@penguintech.group"
LABEL license="GNU AGPL3"

# GET THE FILES WHERE WE NEED THEM!
COPY --from=BUILD /opt/iperf3/* /opt/iperf3/
COPY . /opt/manager/
WORKDIR /opt/manager


# PUT YER ARGS in here
ARG APP_TITLE="PTGAPP" # Change this to actual title for Default

# BUILD IT!
RUN ansible-playbook build.yml -c local

# PUT YER ENVS in here
ENV HELLO="WORLD"

# Switch to non-root user
USER ptg-user

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
