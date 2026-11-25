"""Smoke tests for the CLI skeleton (T01)."""

from __future__ import annotations

from hpat import __version__
from hpat.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_help_lists_all_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("run", "sim", "validate", "list-tests", "bench-check"):
        assert command in result.output


def test_version_option() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_list_tests_returns_empty_registry() -> None:
    result = runner.invoke(app, ["list-tests"])
    assert result.exit_code == 0
    assert "No test items registered yet" in result.output
