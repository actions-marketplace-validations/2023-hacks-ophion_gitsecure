# Container image that runs your code
FROM ubuntu:16.04

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY codes/* /

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    chmod +x /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
