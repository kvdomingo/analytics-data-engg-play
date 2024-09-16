FROM python:3.12-bookworm

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.8.3
ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

RUN apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

WORKDIR /app

ENTRYPOINT [ "/bin/bash", "-c" ]
