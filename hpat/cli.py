"""Command line interface for HP-AT01.

Commands are registered here; the heavy lifting lives in ``hpat.core`` and
``hpat.tests``. Each command is a stub until its task is implemented.
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from hpat import __version__
from hpat.core.bench import check_bench
from hpat.core.config import load_config
from hpat.core.errors import HpatError
from hpat.core.logging_setup import setup_logging
from hpat.core.runfolder import create_run_folder

app = typer.Typer(
    name="hpat",
    help="HP-AT01 - PMIC automated test software.",
    no_args_is_help=True,
    add_completion=False,
)

_CONFIG_OPTION = typer.Option(
    Path("config/instruments.yaml"),
    "--config",
    "-c",
    help="Path to the instrument configuration file.",
)
_DUT_OPTION = typer.Option(
    "NA",
    "--dut-sn",
    help="DUT serial number (used in the run folder name).",
)
_VERBOSE_OPTION = typer.Option(
    False,
    "--verbose",
    "-v",
    help="Enable DEBUG logging (raw SCPI TX/RX).",
)


def _not_implemented(command: str, task: str) -> None:
    typer.secho(f"'{command}' is not implemented yet ({task}).", fg=typer.colors.YELLOW)
    raise typer.Exit(code=2)


@app.command()
def run(
    plan: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        help="Test plan CSV file.",
    ),
    config: Path = _CONFIG_OPTION,
    dut_sn: str = _DUT_OPTION,
    verbose: bool = _VERBOSE_OPTION,
) -> None:
    """Run a test plan on the real bench."""
    try:
        bench = load_config(config)
        run_dir = create_run_folder(Path("runs"), plan, dut_sn)
        logger = setup_logging(run_dir.log_file, verbose)
    except HpatError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    logger.info(
        "preflight ok: %d instruments configured, simulation=%s",
        len(bench.instruments),
        bench.simulation,
    )
    typer.echo(f"Run folder: {run_dir.root}")
    _not_implemented("run", "T05")


@app.command()
def sim(
    plan: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        help="Test plan CSV file.",
    ),
    config: Path = _CONFIG_OPTION,
    dut_sn: str = _DUT_OPTION,
    verbose: bool = _VERBOSE_OPTION,
) -> None:
    """Run a test plan against simulated instruments."""
    _not_implemented("sim", "T05")


@app.command()
def validate(
    plan: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        help="Test plan CSV file.",
    ),
) -> None:
    """Validate a test plan without opening any instrument."""
    _not_implemented("validate", "T05")


@app.command("list-tests")
def list_tests() -> None:
    """List registered test items and their CSV columns."""
    typer.echo("No test items registered yet.")


@app.command("bench-check")
def bench_check(
    config: Path = _CONFIG_OPTION,
    verbose: bool = _VERBOSE_OPTION,
    simulate: bool = typer.Option(
        False,
        "--sim",
        help="Check simulated instruments instead of real ones.",
    ),
) -> None:
    """Check connectivity of every configured instrument."""
    try:
        bench = load_config(config)
    except HpatError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    setup_logging(None, verbose)
    results = check_bench(bench, simulation=simulate or bench.simulation)

    table = Table(title="Bench check")
    table.add_column("Role", style="bold")
    table.add_column("Driver")
    table.add_column("Resource", overflow="fold")
    table.add_column("Status")
    table.add_column("Detail", overflow="fold")
    for result in results:
        status = "[green]OK[/green]" if result.ok else "[red]FAIL[/red]"
        table.add_row(result.role, result.driver, result.resource or "-", status, result.detail)
    Console(width=110).print(table)

    failures = sum(1 for result in results if not result.ok)
    if failures:
        typer.secho(
            f"{failures}/{len(results)} instrument(s) failed.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    typer.secho(f"All {len(results)} instruments OK.", fg=typer.colors.GREEN)


def _version_callback(value: bool | None) -> None:
    if value:
        typer.echo(f"hpat {__version__}")
        raise typer.Exit()


@app.callback()
def _root(
    version: bool | None = typer.Option(
        None,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """HP-AT01 - PMIC automated test software."""


def main() -> None:
    """Console script entry point."""
    app()


if __name__ == "__main__":
    main()
