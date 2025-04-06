ARG OS=bullseye
FROM mcr.microsoft.com/devcontainers/base:$OS AS builder

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update  \
    && apt-get -y install git