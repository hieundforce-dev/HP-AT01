"""CLI tests for ``hpat bench-check`` (T03)."""

from __future__ import annotations

from pathlib import Path

from hpat.cli import app
from typer.testing import CliRunner

runner = CliRunner()

CONFIG = """
instruments:
  psu: {driver: gwinstek_gpd3303s, resource: "ASRL3::INSTR"}
  eload: {driver: eload_3315d, resource: "GPIB0::5::INSTR"}
  scope: {driver: tektronix_tbs2204b, resource: "USB0::0x0699::0x0000::C000000::INSTR"}
  ft232h: {driver: ft232h, resource: "FT232H-A"}
safety:
  max_voltage_v: 12.0
  max_current_a: 20.0
"""


def write_config(tmp_path: Path) -> Path:
    path = tmp_path / "instruments.yaml"
    path.write_text(CONFIG, encoding="utf-8")
    return path


def test_bench_check_sim_all_ok(tmp_path: Path) -> None:
    result = runner.invoke(app, ["bench-check", "--sim", "--config", str(write_config(tmp_path))])

    assert result.exit_code == 0
    assert "OK" in result.output
    assert "All 4 instruments OK." in result.output


def test_bench_check_real_mode_fails_until_drivers_exist(tmp_path: Path) -> None:
    result = runner.invoke(app, ["bench-check", "--config", str(write_config(tmp_path))])

    assert result.exit_code == 1
    assert "FAIL" in result.output
    assert "4/4 instrument(s) failed." in result.output


def test_bench_check_reports_config_error(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("instruments: {}\nsafety: {max_voltage_v: 1, max_current_a: 1}\n")

    result = runner.invoke(app, ["bench-check", "--sim", "--config", str(path)])

    assert result.exit_code == 1
    assert "missing required instrument roles" in result.output
