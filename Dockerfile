FROM ghcr.io/diogenesanalytics/python-testing:master AS testing

# define the build arguments
ARG DCKRSRC

# Install only git, make, and tree, which cookiecutter or hooks might need
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    tree \
 && rm -rf /var/lib/apt/lists/*

# turn off poetry venv
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR ${DCKRSRC}

COPY . .

RUN poetry install --with test,lint --no-root -C .
