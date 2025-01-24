FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.0.1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

RUN apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python -

ENTRYPOINT [ "/bin/bash", "-euxo", "pipefail", "-c" ]
