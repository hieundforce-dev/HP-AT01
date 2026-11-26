"""GPIO on the FT232H ACBUS pins (T04).

ADBUS0/ADBUS1/ADBUS2 are reserved for I2C, so the eight GPIO lines are
ACBUS0-ACBUS7 (``pin`` 0-7). All pins start as **inputs** with a low latch so
that connecting the board never drives the DUT; a pin must be configured as an
output (implicitly done by :meth:`write`) before it can drive a level.
"""

from __future__ import annotations

from hpat.core.errors import InstrumentError
from hpat.drivers.ft232h_mpsse import (
    READ_BITS_HIGH,
    SEND_IMMEDIATE,
    SET_BITS_HIGH,
    Transport,
)

GPIO_PIN_COUNT = 8


class MpsseGpio:
    """Eight GPIO lines (ACBUS0-7) with direction control."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport
        self._value = 0
        self._direction = 0  # 1 = output

    def configure(self) -> None:
        """Put every GPIO in input mode with a low latch."""
        self._value = 0
        self._direction = 0
        self._apply()

    @staticmethod
    def _check_pin(pin: int) -> None:
        if not 0 <= pin < GPIO_PIN_COUNT:
            raise ValueError(f"GPIO pin must be 0-{GPIO_PIN_COUNT - 1}, got {pin!r}")

    def set_direction(self, pin: int, output: bool) -> None:
        """Configure ``pin`` as an output or an input."""
        self._check_pin(pin)
        if output:
            self._direction |= 1 << pin
        else:
            self._direction &= ~(1 << pin)
        self._apply()

    def write(self, pin: int, level: bool) -> None:
        """Drive ``pin`` high or low; the pin is switched to output if needed."""
        self._check_pin(pin)
        if not self._direction & (1 << pin):
            self._direction |= 1 << pin
        if level:
            self._value |= 1 << pin
        else:
            self._value &= ~(1 << pin)
        self._apply()

    def read(self, pin: int) -> bool:
        """Read the level currently seen on ``pin`` (input or output read-back)."""
        self._check_pin(pin)
        return bool(self.read_all() & (1 << pin))

    def read_all(self) -> int:
        """Return the 8 ACBUS levels as a bit mask."""
        self._transport.write(bytes([READ_BITS_HIGH, SEND_IMMEDIATE]))
        response = self._transport.read(1)
        return response[0]

    def _apply(self) -> None:
        self._transport.write(bytes([SET_BITS_HIGH, self._value & 0xFF, self._direction & 0xFF]))


class GpioError(InstrumentError):
    """GPIO operation failed."""
