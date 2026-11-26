"""Tests for the driver registry and bench check (T03)."""

from __future__ import annotations

import pytest
from hpat.core.bench import check_bench
from hpat.core.config import BenchConfig, InstrumentConfig, SafetyConfig
from hpat.core.errors import InstrumentError
from hpat.drivers import ft232h_driver
from hpat.drivers.ft232h_driver import Ft232hDriver
from hpat.drivers.ft232h_mpsse import MpsseError
from hpat.drivers.registry import create_instrument
from hpat.drivers.sim import SimFt232h, SimPsu


def make_config(drivers: dict[str, str] | None = None) -> BenchConfig:
    drivers = drivers or {
        "psu": "gwinstek_gpd3303s",
        "eload": "prodigit_3315g",
        "scope": "tektronix_tbs2204b",
        "ft232h": "ft232h",
        "dmm_vin": "dmm_ut8805e",
    }
    return BenchConfig(
        instruments={
            role: InstrumentConfig(driver=driver, resource=f"RES::{role}")
            for role, driver in drivers.items()
        },
        safety=SafetyConfig(max_voltage_v=12.0, max_current_a=20.0),
    )


def test_registry_returns_simulated_driver() -> None:
    config = make_config()
    instrument = create_instrument("psu", config.instruments["psu"], simulation=True)
    assert isinstance(instrument, SimPsu)


def test_registry_returns_ft232h_sim() -> None:
    config = make_config()
    instrument = create_instrument("ft232h", config.instruments["ft232h"], simulation=True)
    assert isinstance(instrument, SimFt232h)


def test_registry_returns_ft232h_real_driver() -> None:
    config = make_config()
    instrument = create_instrument("ft232h", config.instruments["ft232h"], simulation=False)
    assert isinstance(instrument, Ft232hDriver)


def test_registry_rejects_unknown_driver() -> None:
    config = InstrumentConfig(driver="does_not_exist", resource="X")
    with pytest.raises(InstrumentError, match="unknown driver 'does_not_exist'"):
        create_instrument("psu", config, simulation=True)


def test_registry_real_mode_reports_missing_implementation() -> None:
    config = make_config()
    with pytest.raises(InstrumentError, match="no real implementation yet"):
        create_instrument("psu", config.instruments["psu"], simulation=False)


def test_check_bench_simulated_all_ok() -> None:
    results = check_bench(make_config(), simulation=True)

    assert len(results) == 5
    assert all(result.ok for result in results)
    assert all(result.detail.startswith("SIM,") for result in results)


def test_check_bench_real_mode_reports_every_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(**_kwargs: object) -> None:
        raise MpsseError("FT232H: D2XX library not available")

    monkeypatch.setattr(ft232h_driver, "open_ft232h", fail)
    results = {result.role: result for result in check_bench(make_config(), simulation=False)}

    assert len(results) == 5
    assert not any(result.ok for result in results.values())
    for role in ("psu", "eload", "scope", "dmm_vin"):
        assert "no real implementation yet" in results[role].detail
    assert "D2XX library not available" in results["ft232h"].detail


def test_check_bench_unknown_driver_is_isolated() -> None:
    config = make_config(
        {
            "psu": "gwinstek_gpd3303s",
            "eload": "prodigit_3315g",
            "scope": "tektronix_tbs2204b",
            "ft232h": "ft232h",
            "dmm_vin": "nope",
        }
    )
    results = {result.role: result for result in check_bench(config, simulation=True)}

    assert results["psu"].ok is True
    assert results["dmm_vin"].ok is False
    assert "unknown driver 'nope'" in results["dmm_vin"].detail


def test_sim_psu_tracks_setpoints_and_output() -> None:
    config = make_config()
    psu = create_instrument("psu", config.instruments["psu"], simulation=True)

    psu.write("VSET1:5.00")
    psu.write("ISET1:1.500")
    assert psu.query("VOUT1?") == "0.000"  # output still off

    psu.write("OUT1")
    assert psu.query("VOUT1?") == "5.000"
    assert psu.query("IOUT1?") == "1.500"
