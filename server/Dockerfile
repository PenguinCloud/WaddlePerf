FROM ghcr.io/penguincloud/core
LABEL company="Penguin Technologies Inc."
LABEL org.opencontainers.image.authors="info@penguintech.io"
LABEL license="GNU AGPL3"
# GET THE FILES WHERE WE NEED THEM!
COPY . /opt/manager/
COPY libs/speedtest/ /var/www/speedtest
WORKDIR /opt/manager
RUN apt update 
# PUT YER ARGS in here
ARG APP_TITLE="WADDLEPERF" # Change this to actual title for Default
ARG BUILD_THREADS="4"
ARG RUN_AUTOUPDATES="true"
# IPERF ARGS
ARG IPERF_URL="https://github.com/esnet/iperf/archive/refs/tags/3.14.tar.gz"
# S3
ARG S3_ENABLED="true"

# BUILD IT!
#RUN /usr/bin/bash bins/py4web.py # This is coming later
RUN ansible-playbook entrypoint.yml -c local --tags build
#------------------------------------------------------------------#
# General Environment variables
ENV APP_TITLE="WADDLEPERF-SERVER"
# IPERF Environment variables
ENV IPERF_SERVER_ENABLED="true"
ENV IPERF_SERVER_IP="127.0.0.1"
ENV IPERF_SERVER_PORT="5201"
ENV IPERF_CLIENT_STREAMS="1"
ENV IPERF_CLIENT_ENABLED="true"
ENV IPERF_CLIENT_BITRATE="100M"
ENV IPERF_CLIENT_RETURN="1"
ENV IPERF_CLIENT_LOGFILE="0"
ENV IPERF_PASSWORD="changemeplease"
ENV IPERF_USERNAME="www-data"
ENV IPERF_PROTOCOL="tcp"
ENV IPERF_AUTHENTICATION="1"
# NGINX Environment variables
ENV WEB_PORT="80"
ENV WEB_SPORT="443"
ENV WEB_HOST="localhost"

# S3
ENV S3_ENABLED="false"
ENV S3_INTERVAL="10"
ENV S3_URL="http://localhost"
ENV S3_BUCKET="changeme"
ENV S3_ENCRYPT="true"
ENV S3_COMPATIBILITY="true"
ENV S3_KEY_ACCESS="key_example_access"
ENV S3_KEY_SECRET="SUPERSECRETSQUIRREL_EXAMPLE"
# HealthCheck
ENV HEALTHCHECK_ENABLED="true"
ENV HEALTHCHECK_INTERVAL="10"

# Results drop off location
ENV RESULTS_DIR="/var/www/waddleperf"
ENV RESULTS_FILE="results.json"

# iPerf Server
EXPOSE 5201 
# SpeedTest Web UI
EXPOSE 80 
#If you want HTTPS, for now, put a reverse proxy in front of this host for web traffic

RUN chown -R www-data:www-data /var/lib/nginx && chown -R www-data:www-data /usr/share/nginx
# Switch to non-root user
USER www-data
# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
