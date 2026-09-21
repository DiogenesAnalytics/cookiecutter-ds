[![tests](https://github.com/DiogenesAnalytics/cookiecutter-ds/actions/workflows/tests.yml/badge.svg)](https://github.com/DiogenesAnalytics/cookiecutter-ds/actions/workflows/tests.yml)
[![docker](https://github.com/DiogenesAnalytics/cookiecutter-ds/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/DiogenesAnalytics/cookiecutter-ds/actions/workflows/docker-publish.yml)

# Cookiecutter Data Science

*A logical, reasonably standardized, but flexible project structure for doing and sharing data science work.*

This repository provides a Cookiecutter template for creating data science projects with a standardized project structure and a Docker-based Jupyter development environment.

## Requirements

* Python 3.9–3.12
* [Cookiecutter](https://cookiecutter.readthedocs.io/)
* Docker

Install Cookiecutter with pip:

```bash
pip install cookiecutter
```

## Creating a New Project

Run Cookiecutter against this repository:

```bash
cookiecutter https://github.com/DiogenesAnalytics/cookiecutter-ds.git
```

Cookiecutter will prompt for the project configuration, including the project name, author, GitHub account, description, and license.

The generated project uses the configured Docker image for its Jupyter development environment.

## Generated Project Structure

The template currently generates the following project structure:

```text
├── LICENSE
├── Makefile
├── README.md
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── models
├── notebooks
│   └── template_report.ipynb
├── references
│   └── cited_report.bib
├── reports
│   ├── figures
│   └── templates
│       └── cited_report
│           ├── conf.json
│           └── index.tex.j2
└── src
    ├── data
    │   ├── __init__.py
    │   └── make_dataset.py
    ├── features
    │   ├── __init__.py
    │   └── build_features.py
    ├── models
    │   ├── __init__.py
    │   ├── predict_model.py
    │   └── train_model.py
    ├── visualization
    │   ├── __init__.py
    │   └── visualize.py
    ├── __init__.py
    ├── jupyter_report.py
    └── web_images.py
```

The generated project is intentionally flexible. The template provides a useful starting structure without prescribing how individual analyses, models, or data-processing workflows must be implemented.

## Development

The template itself is developed and tested separately from the projects it generates.

Install the development dependencies with Poetry:

```bash
poetry install --with test,lint
```

### Running Tests

The test suite uses `pytest` and `pytest-cookies` to generate projects from the template and verify their structure and contents.

```bash
pytest
```

### Running the Checks

The repository also provides Make targets for running the test and linting suite in the project's Docker testing environment.

```bash
make tests
make check-all
```

See the `Makefile` for the complete set of available development commands.

## License

This project is distributed under the MIT License.
