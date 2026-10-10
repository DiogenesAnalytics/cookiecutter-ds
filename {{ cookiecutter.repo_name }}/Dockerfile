# ------------------------------------------------------------------------------
# Data science project environment
# ------------------------------------------------------------------------------

FROM ghcr.io/diogenesanalytics/scipy-notebook:master

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# ------------------------------------------------------------------------------
# System dependencies for nbreport PDF export
# ------------------------------------------------------------------------------

USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
        pandoc \
        texlive-xetex \
        lmodern \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# Configure Poetry
# ------------------------------------------------------------------------------

USER ${NB_UID}

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR "${HOME}"

# ------------------------------------------------------------------------------
# Install project dependencies
# ------------------------------------------------------------------------------

COPY --chown=${NB_UID}:${NB_GID} pyproject.toml ./

RUN poetry install --with dev --no-root

# ------------------------------------------------------------------------------
# Copy project files
# ------------------------------------------------------------------------------

COPY --chown=${NB_UID}:${NB_GID} . .

# ------------------------------------------------------------------------------
# Runtime context
# ------------------------------------------------------------------------------

WORKDIR "${HOME}"
