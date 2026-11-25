"""Bench operations: open configured instruments and report their status."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from hpat.core.config import BenchConfig, InstrumentConfig
from hpat.core.errors import HpatError
from hpat.drivers.base import Instrument
from hpat.drivers.registry import create_instrument

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CheckResult:
    """Outcome of checking one configured instrument."""

    role: str
    driver: str
    resource: str
    ok: bool
    detail: str


def _result(role: str, config: InstrumentConfig, ok: bool, detail: str) -> CheckResult:
    return CheckResult(
        role=role, driver=config.driver, resource=config.resource, ok=ok, detail=detail
    )


def check_bench(config: BenchConfig, simulation: bool | None = None) -> list[CheckResult]:
    """Open, identify and close every configured instrument.

    Args:
        config: Validated bench configuration.
        simulation: Force simulated drivers. Defaults to ``config.simulation``.

    Returns:
        One result per configured role, in configuration order. Failures are
        reported in ``detail`` instead of raising, so one bad instrument does
        not hide the state of the others.
    """
    sim = config.simulation if simulation is None else simulation
    results: list[CheckResult] = []

    for role, instrument_config in config.instruments.items():
        instrument: Instrument | None = None
        try:
            instrument = create_instrument(role, instrument_config, simulation=sim)
            instrument.open()
            detail = instrument.identify()
            results.append(_result(role, instrument_config, True, detail))
            logger.debug("%s OK: %s", role, detail)
        except HpatError as exc:
            results.append(_result(role, instrument_config, False, str(exc)))
            logger.error("%s FAILED: %s", role, exc)
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"
            results.append(_result(role, instrument_config, False, detail))
            logger.error("%s FAILED: %s", role, detail)
        finally:
            if instrument is not None:
                instrument.close()

    return results
