"""Tests for the ``run`` preflight (config + run folder) added in T02."""

from __future__ import annotations

from pathlib import Path

from hpat.cli import app
from typer.testing import CliRunner

runner = CliRunner()

VALID_CONFIG = """
instruments:
  psu: {driver: gwinstek_gpd3303s, resource: "ASRL3::INSTR"}
  eload: {driver: eload_3315d, resource: "GPIB0::5::INSTR"}
  scope: {driver: tektronix_tbs2204b, resource: "USB0::0x0699::0x0000::C000000::INSTR"}
  ft232h: {driver: ft232h, resource: "FT232H-A"}
safety:
  max_voltage_v: 12.0
  max_current_a: 20.0
"""


def prepare(tmp_path: Path, monkeypatch, config_text: str = VALID_CONFIG) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "plan.csv").write_text("test_id\nEFF_BUCK1\n", encoding="utf-8")
    (tmp_path / "instruments.yaml").write_text(config_text, encoding="utf-8")


def test_run_preflight_creates_run_folder(tmp_path: Path, monkeypatch) -> None:
    prepare(tmp_path, monkeypatch)

    result = runner.invoke(
        app,
        ["run", "plan.csv", "--config", "instruments.yaml", "--dut-sn", "SN123"],
    )

    assert result.exit_code == 2
    assert "Run folder:" in result.output
    runs = list((tmp_path / "runs").iterdir())
    assert len(runs) == 1
    assert runs[0].name.endswith("_plan_SN123")
    assert (runs[0] / "results").is_dir()
    assert (runs[0] / "logs" / "run.log").is_file()


def test_run_reports_config_error(tmp_path: Path, monkeypatch) -> None:
    prepare(tmp_path, monkeypatch, VALID_CONFIG.replace("  ft232h:", "  ft232x:"))

    result = runner.invoke(app, ["run", "plan.csv", "--config", "instruments.yaml"])

    assert result.exit_code == 1
    assert "unknown instrument roles: ft232x" in result.output
