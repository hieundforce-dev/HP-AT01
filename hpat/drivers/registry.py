"""Driver registry: maps a configured driver name to a driver class.

Real drivers are registered here as they are implemented (T07-T09). Until
then, only the simulated drivers exist, so ``bench-check`` without ``--sim``
reports a clear "not implemented yet" error instead of touching hardware.
"""

from __future__ import annotations

from hpat.core.config import InstrumentConfig
from hpat.core.errors import InstrumentError
from hpat.drivers.base import Instrument
from hpat.drivers.sim.instruments import (
    SimEload,
    SimFt232h,
    SimKeithley2000,
    SimKeithley2100,
    SimPsu,
    SimScope,
    SimUt8805E,
)

SIM_DRIVERS: dict[str, type[Instrument]] = {
    "gwinstek_gpd3303s": SimPsu,
    "eload_3315d": SimEload,
    "tektronix_tbs2204b": SimScope,
    "dmm_ut8805e": SimUt8805E,
    "dmm_keithley2000": SimKeithley2000,
    "dmm_keithley2100": SimKeithley2100,
    "ft232h": SimFt232h,
}

#: Filled in by later tasks (T04, T07, T08, T09).
REAL_DRIVERS: dict[str, type[Instrument]] = {}


def create_instrument(
    role: str,
    config: InstrumentConfig,
    simulation: bool,
) -> Instrument:
    """Instantiate the driver configured for ``role``.

    Raises:
        InstrumentError: the driver name is unknown, or only a simulation
            exists while ``simulation`` is false.
    """
    drivers = SIM_DRIVERS if simulation else REAL_DRIVERS
    driver_class = drivers.get(config.driver)
    if driver_class is not None:
        return driver_class(role, config)

    if not simulation and config.driver in SIM_DRIVERS:
        raise InstrumentError(
            f"{role}: driver '{config.driver}' has no real implementation yet "
            "(run with --sim to use the simulated bench)"
        )
    raise InstrumentError(f"{role}: unknown driver '{config.driver}' (simulation={simulation})")
