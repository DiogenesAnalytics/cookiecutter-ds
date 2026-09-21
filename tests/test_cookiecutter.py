"""Tests for the Cookiecutter template."""

import py_compile
from pathlib import Path
from typing import List

import pytest
from pytest_cookies.plugin import Cookies
from pytest_cookies.plugin import Result


def test_default_project_generation(default_baked_project: Result) -> None:
    """Ensure the template bakes cleanly using default context.

    Args:
        default_baked_project: The result of baking the default template.
    """
    assert default_baked_project.exit_code == 0
    assert default_baked_project.exception is None
    assert default_baked_project.project_path.is_dir()


def test_project_structure(
    default_baked_project: Result, project_dir_structure: List[str]
) -> None:
    """Verify generated project contains the expected files and directories.

    Args:
        default_baked_project: The result of baking the default template.
        project_dir_structure: Expected files and directories in the generated project.
    """
    project_path: Path = default_baked_project.project_path

    missing = [
        item for item in project_dir_structure if not (project_path / item).exists()
    ]

    assert not missing, f"Missing expected files/directories: {missing}"


def test_custom_project_generation(cookies: Cookies) -> None:
    """Ensure custom project values are rendered correctly.

    Args:
        cookies: The pytest-cookies fixture.
    """
    result = cookies.bake(
        extra_context={
            "project_name": "my-test-project",
            "github_name": "TestUser",
            "author_name": "Test Author",
            "description": "A test project.",
            "open_source_license": "MIT",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == "my-test-project"


@pytest.mark.parametrize(
    "license_name,expected_text",
    [
        ("MIT", "The MIT License (MIT)"),
        ("BSD-3-Clause", "Redistribution and use in source and binary forms"),
        ("No license file", ""),
    ],
)
def test_license_generation(
    cookies: Cookies, license_name: str, expected_text: str
) -> None:
    """Verify license selection controls LICENSE contents.

    Args:
        cookies: The pytest-cookies fixture.
        license_name: License selected for the generated project.
        expected_text: Text expected in the generated LICENSE file.
    """
    result = cookies.bake(
        extra_context={"open_source_license": license_name},
    )

    assert result.exit_code == 0
    assert result.exception is None

    license_path = result.project_path / "LICENSE"

    assert license_path.is_file()

    contents = license_path.read_text()

    assert expected_text in contents


def test_repo_name_transformation(cookies: Cookies) -> None:
    """Verify project names are converted to repository names.

    Args:
        cookies: The pytest-cookies fixture.
    """
    result = cookies.bake(
        extra_context={
            "project_name": "My Awesome Project",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "my_awesome_project"


def test_no_unrendered_cookiecutter_variables(
    default_baked_project: Result,
) -> None:
    """Ensure generated files contain no unrendered Cookiecutter variables.

    Args:
        default_baked_project: The generated project.
    """
    project_path: Path = default_baked_project.project_path

    for path in project_path.rglob("*"):
        if not path.is_file():
            continue

        try:
            contents = path.read_text()
        except UnicodeDecodeError:
            continue

        assert "{{ cookiecutter." not in contents, path


def test_generated_readme(
    default_baked_project: Result,
) -> None:
    """Verify generated README contains expected project metadata.

    Args:
        default_baked_project: The generated project.
    """
    readme_path = default_baked_project.project_path / "README.md"

    contents = readme_path.read_text()

    assert "project_name" in contents
    assert "A short description of the project." in contents


def test_generated_python(
    default_baked_project: Result,
) -> None:
    """Verify generated Python files compile successfully.

    Args:
        default_baked_project: The generated project.
    """
    project_path = default_baked_project.project_path

    for path in project_path.rglob("*.py"):
        py_compile.compile(path, doraise=True)
