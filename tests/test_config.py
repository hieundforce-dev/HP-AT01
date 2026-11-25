"""Tests for the instrument configuration loader (T02)."""

from __future__ import annotations

from pathlib import Path

import pytest
from hpat.core.config import BenchConfig, load_config
from hpat.core.errors import ConfigError

VALID_CONFIG = """
instruments:
  psu:
    driver: gwinstek_gpd3303s
    resource: "ASRL3::INSTR"
    options: {channel: 1}
  eload:
    driver: eload_3315d
    resource: "GPIB0::5::INSTR"
  scope:
    driver: tektronix_tbs2204b
    resource: "USB0::0x0699::0x0000::C000000::INSTR"
  ft232h:
    driver: ft232h
    resource: "FT232H-A"
safety:
  max_voltage_v: 12.0
  max_current_a: 20.0
"""


def write_config(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "instruments.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_load_valid_config(tmp_path: Path) -> None:
    config = load_config(write_config(tmp_path, VALID_CONFIG))

    assert isinstance(config, BenchConfig)
    assert config.simulation is False
    assert set(config.instruments) == {"psu", "eload", "scope", "ft232h"}
    assert config.instruments["psu"].options["channel"] == 1
    assert config.safety.settle_ms_default == 200
    assert config.safety.power_down_order == ["eload", "psu"]


def test_missing_required_role_is_reported(tmp_path: Path) -> None:
    text = VALID_CONFIG.replace(
        "  scope:\n"
        "    driver: tektronix_tbs2204b\n"
        '    resource: "USB0::0x0699::0x0000::C000000::INSTR"\n',
        "",
    )
    with pytest.raises(ConfigError, match="missing required instrument roles: scope"):
        load_config(write_config(tmp_path, text))


def test_unknown_role_is_reported(tmp_path: Path) -> None:
    text = VALID_CONFIG.replace("  ft232h:", "  ft232x:")
    with pytest.raises(ConfigError, match="unknown instrument roles: ft232x"):
        load_config(write_config(tmp_path, text))


def test_field_error_names_the_field(tmp_path: Path) -> None:
    text = VALID_CONFIG.replace("max_voltage_v: 12.0", "max_voltage_v: -1")
    with pytest.raises(ConfigError) as excinfo:
        load_config(write_config(tmp_path, text))
    assert "safety.max_voltage_v" in str(excinfo.value)


def test_missing_file_is_reported(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="Config file not found"):
        load_config(tmp_path / "nope.yaml")


def test_invalid_yaml_reports_location(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="Invalid YAML"):
        load_config(write_config(tmp_path, "instruments: [unclosed\n"))


def test_empty_file_is_reported(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="empty"):
        load_config(write_config(tmp_path, ""))


def test_unknown_top_level_key_is_reported(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="unexpected_key"):
        load_config(write_config(tmp_path, VALID_CONFIG + "\nunexpected_key: 1\n"))


def test_instrument_lookup_of_unconfigured_role(tmp_path: Path) -> None:
    config = load_config(write_config(tmp_path, VALID_CONFIG))
    with pytest.raises(ConfigError, match="dmm_vout"):
        config.instrument("dmm_vout")
