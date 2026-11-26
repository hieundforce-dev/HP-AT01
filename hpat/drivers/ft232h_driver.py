"""FT232H instrument driver: I2C + GPIO over MPSSE (T04).

The public API matches the simulated driver (``SimFt232h``) so test items do
not care whether they talk to hardware or to the simulator::

    driver.i2c_write(address, register, value)
    driver.i2c_read(address, register) -> int
    driver.set_gpio(pin, level)
    driver.read_gpio(pin) -> bool

Extra methods for multi-byte access and bus scanning are available for tests
that need them (``i2c_write_bytes``, ``i2c_read_bytes``, ``i2c_scan``).
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

from hpat.core.config import InstrumentConfig
from hpat.core.errors import InstrumentError
from hpat.drivers.base import Instrument
from hpat.drivers.ft232h_gpio import MpsseGpio
from hpat.drivers.ft232h_i2c import MpsseI2C
from hpat.drivers.ft232h_mpsse import (
    FtdiTransport,
    Transport,
    ft232h_label,
    open_ft232h,
)

logger = logging.getLogger(__name__)


class Ft232hDriver(Instrument):
    """FT232H bridge in MPSSE mode (I2C master + 8 GPIO lines)."""

    def __init__(
        self,
        role: str,
        config: InstrumentConfig,
        transport: Transport | None = None,
        device: Any | None = None,
        label: str | None = None,
    ) -> None:
        super().__init__(role, config)
        self._transport = transport
        self._device = device
        self._label = label
        self._i2c: MpsseI2C | None = None
        self._gpio: MpsseGpio | None = None

    # -- lifecycle ---------------------------------------------------------
    def open(self) -> None:
        if self._i2c is not None:
            return

        timeout_s = self._float_option("timeout_s", 2.0)
        if self._transport is None:
            serial = str(self.config.options.get("serial", "") or "")
            index = self._int_option("index", 0)
            self._device = open_ft232h(serial=serial, index=index, timeout_s=timeout_s)
            self._label = ft232h_label(self._device)
            self._transport = FtdiTransport(self._device, timeout_s=timeout_s)
        elif self._label is None:
            self._label = "FTDI,FT232H,INJECTED"

        clock_hz = self._float_option("i2c_frequency_hz", self._float_option("clock_hz", 100_000.0))
        self._i2c = MpsseI2C(
            self._transport,
            clock_hz=clock_hz,
            clock_stretching=self._bool_option("clock_stretching", False),
            nop_cycles_send=self._int_option("nop_cycles_send", 1),
            nop_cycles_read=self._int_option("nop_cycles_read", 1),
        )
        self._i2c.configure()
        self._gpio = MpsseGpio(self._transport)
        self._gpio.configure()
        logger.debug("%s opened: %s at %.0f Hz", self.role, self._label, clock_hz)

    def close(self) -> None:
        if self._device is not None:
            try:
                self._device.close()
            except Exception as exc:  # closing must never mask the original error
                logger.warning("%s: error while closing FT232H: %s", self.role, exc)
            finally:
                self._device = None
        self._transport = None
        self._i2c = None
        self._gpio = None

    def identify(self) -> str:
        if self._label is None:
            raise InstrumentError(f"{self.role}: FT232H is not open")
        return self._label

    # -- options -----------------------------------------------------------
    def _int_option(self, key: str, default: int) -> int:
        try:
            return int(self.config.options.get(key, default))
        except (TypeError, ValueError) as exc:
            raise InstrumentError(
                f"{self.role}: option '{key}' must be an integer, "
                f"got {self.config.options.get(key)!r}"
            ) from exc

    def _float_option(self, key: str, default: float) -> float:
        try:
            return float(self.config.options.get(key, default))
        except (TypeError, ValueError) as exc:
            raise InstrumentError(
                f"{self.role}: option '{key}' must be a number, "
                f"got {self.config.options.get(key)!r}"
            ) from exc

    def _bool_option(self, key: str, default: bool) -> bool:
        value = self.config.options.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on"}
        return bool(value)

    # -- I2C ---------------------------------------------------------------
    def _require_open(self) -> tuple[MpsseI2C, MpsseGpio]:
        if self._i2c is None or self._gpio is None:
            raise InstrumentError(f"{self.role}: FT232H is not open")
        return self._i2c, self._gpio

    def i2c_write(self, address: int, register: int, value: int) -> None:
        """Write one byte to an 8-bit register."""
        i2c, _ = self._require_open()
        i2c.write_register(address, register, [value & 0xFF])

    def i2c_read(self, address: int, register: int) -> int:
        """Read one byte from an 8-bit register."""
        i2c, _ = self._require_open()
        return i2c.read_register(address, register, count=1)[0]

    def i2c_write_bytes(self, address: int, register: int, data: Sequence[int]) -> None:
        """Write several bytes starting at an 8-bit register."""
        i2c, _ = self._require_open()
        i2c.write_register(address, register, data)

    def i2c_read_bytes(self, address: int, register: int, count: int) -> list[int]:
        """Read several bytes starting at an 8-bit register."""
        i2c, _ = self._require_open()
        return i2c.read_register(address, register, count=count)

    def i2c_scan(self, first: int = 0x08, last: int = 0x77) -> list[int]:
        """Return the 7-bit addresses that acknowledge a probe."""
        i2c, _ = self._require_open()
        return i2c.scan(first=first, last=last)

    # -- GPIO --------------------------------------------------------------
    def set_gpio(self, pin: int, level: bool) -> None:
        """Drive ACBUS ``pin`` (0-7) high or low."""
        _, gpio = self._require_open()
        gpio.write(pin, level)

    def read_gpio(self, pin: int) -> bool:
        """Read the level on ACBUS ``pin`` (0-7)."""
        _, gpio = self._require_open()
        return gpio.read(pin)

    def configure_gpio(self, pin: int, output: bool) -> None:
        """Configure ACBUS ``pin`` (0-7) as an output or input."""
        _, gpio = self._require_open()
        gpio.set_direction(pin, output)
