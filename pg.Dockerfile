FROM ghcr.io/kvdomingo/postgresql-pig:18

USER root

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]
RUN apt-get update &&  \
    pig ext install pg_duckdb -y &&  \
    apt-get clean &&  \
    rm -rf /var/lib/apt/lists/*

USER 999
