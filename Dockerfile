FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_VERSION=0.8.19
ENV PATH="/home/dagster/.local/bin:/home/dagster/.cargo/bin:${PATH}"

USER root

WORKDIR /tmp

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]
# hadolint ignore=DL3009
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates

ADD https://deb.nodesource.com/setup_22.x nodesource_setup.sh

VOLUME [ "/app/.venv" ]

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]
RUN chmod +x /tmp/nodesource_setup.sh && \
    /tmp/nodesource_setup.sh && \
    apt-get install -y --no-install-recommends nodejs && \
    useradd --uid 1000 --shell /bin/bash --user-group --create-home dagster && \
    mkdir -p /app/.venv && \
    mkdir -p /home/dagster/.tmp && \
    chown -R 1000:1000 /app

ADD https://astral.sh/uv/${UV_VERSION}/install.sh /home/dagster/.tmp/install-uv.sh

RUN chown -R 1000:1000 /home/dagster && \
    chmod +x /home/dagster/.tmp/install-uv.sh

WORKDIR /app

USER dagster

SHELL [ "/bin/sh", "-eu", "-c" ]
RUN /home/dagster/.tmp/install-uv.sh && \
    uv tool install dagster-dg

ENTRYPOINT [ "/bin/bash", "-euxo", "pipefail", "-c" ]
