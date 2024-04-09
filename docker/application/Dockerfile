FROM python:3.10.6-slim AS poetry
ENV TZ=Etc/UTC

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  # do not buffer stdout/stderr, gives output directly to docker log
  PYTHONUNBUFFERED=1 \
  # disable writing of .pyc files on the import of source modules
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.4.2 \
  POETRY_HOME="/opt/poetry" \
  PATH="$PATH:/opt/poetry/bin" \
  # virtual environment for application
  VIRTUAL_ENV=/app/venv

ARG USERNAME=vto_poc
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# docker group ID. 127 is the value in github pipeline
ARG DOCKER_GID=127
# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
  && groupadd --gid $DOCKER_GID docker \
  && useradd --uid $USER_UID --gid $USER_GID --groups docker -m $USERNAME -s /bin/bash

RUN apt-get update \
  && apt-get install --no-install-recommends -y curl \
  && rm -rf /var/lib/apt/lists/*

RUN curl -sSL 'https://install.python-poetry.org' | python -
RUN pip install poetry-dynamic-versioning

USER $USERNAME
WORKDIR /app/vto_poc

# create and activate virtual environment
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install production dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root --no-ansi

##########################################
# dev stage, used for testing + building #
##########################################
FROM poetry AS build

# install dev dependencies
RUN poetry install --no-root --no-ansi

# copy the actual application
RUN pwd
COPY . .

# Versioning
ARG VERSION=0.1.0-dev0
RUN sed -i "/^version = /s/0.1.0/${VERSION}/" pyproject.toml

# Build wheel
RUN poetry build -f wheel

#######################################################
# development container used for developing in VSCode #
#######################################################
FROM poetry AS dev
USER root

RUN apt-get update \
  && apt-get install -y ssh pre-commit git sudo \
  && apt-get update \
  && rm -rf /var/lib/apt/lists/*

# RUN apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly

# allow dev container user to sudo
# RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#   && chmod 0440 /etc/sudoers.d/$USERNAME \
#   && chown -R $USER_UID:$USER_GID /app

USER $USERNAME

##############################
# Application stage, default #
##############################
FROM python:3.10.6-slim AS app
ENV TZ=Etc/UTC

WORKDIR /app/vto_poc

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# activate virtual environment
ENV VIRTUAL_ENV=/app/venv \
  PATH="/app/venv/bin:$PATH"
# copy and install app
COPY --from=poetry /app/venv /app/venv
COPY --from=build /app/vto_poc/dist/*.whl dist/
RUN find dist -type f | xargs pip install --disable-pip-version-check --no-cache --no-deps
