"""I2C master on top of the FT232H MPSSE engine (T04).

The command sequences are adapted from the MIT-licensed reference
implementation ``cyangy/ftdi_mpsse_python`` (``mpsse_i2c.py``), which was
verified on the project bench. Only the FT232H (Drive-Zero open-drain) path is
implemented.

Supported:
    * 7-bit addresses (0x00-0x7F), 8-bit register addresses
    * single and multi-byte writes / reads
    * repeated START for register reads
    * ACK/NACK checking on every byte
    * bus scan
    * optional clock stretching (MPSSE adaptive clocking)

Limitations:
    * 10-bit addresses and SMBus PEC are not implemented.
    * Clock stretching relies on MPSSE adaptive clocking and on the wiring
      described in :mod:`hpat.drivers.ft232h_mpsse`; it is disabled by default.
"""

from __future__ import annotations

from collections.abc import Sequence

from hpat.core.errors import InstrumentError
from hpat.drivers.ft232h_mpsse import (
    ADBUS_I2C_DIRECTION,
    BAD_COMMAND,
    BAD_COMMAND_ECHO,
    CLOCK_BITS_IN_NEG_MSB,
    CLOCK_BITS_OUT_POS_MSB,
    CLOCK_BYTES_IN_NEG_MSB,
    CLOCK_BYTES_OUT_POS_MSB,
    DISABLE_ADAPTIVE_CLOCK,
    DISABLE_CLOCK_DIV5,
    DISABLE_LOOPBACK,
    DRIVE_ZERO,
    ENABLE_3_PHASE,
    ENABLE_ADAPTIVE_CLOCK,
    SDA_HIGH_SCL_HIGH,
    SDA_HIGH_SCL_LOW,
    SDA_LOW_SCL_HIGH,
    SDA_LOW_SCL_LOW,
    SEND_IMMEDIATE,
    SET_BITS_LOW,
    SET_CLOCK_DIVISOR,
    Transport,
    clock_divisor,
)

#: Number of repeated ``SET_BITS_LOW`` commands per START/STOP stage. This is
#: the value used by the verified reference implementation and gives the bus
#: enough time to settle with open-drain lines.
SETUP_CYCLES = 30


class I2cError(InstrumentError):
    """I2C transaction failed."""


class I2cNackError(I2cError):
    """A slave did not acknowledge a byte."""


class MpsseI2C:
    """Minimal I2C master driven through MPSSE commands."""

    def __init__(
        self,
        transport: Transport,
        clock_hz: float = 100_000,
        clock_stretching: bool = False,
        nop_cycles_send: int = 1,
        nop_cycles_read: int = 1,
        setup_cycles: int = SETUP_CYCLES,
    ) -> None:
        self._transport = transport
        self.clock_hz = float(clock_hz)
        self.clock_stretching = bool(clock_stretching)
        self._nop_send = max(1, int(nop_cycles_send))
        self._nop_read = max(1, int(nop_cycles_read))
        self._setup_cycles = max(1, int(setup_cycles))
        self._divisor = clock_divisor(self.clock_hz)
        self._start_cmd = self._build_start()
        self._stop_cmd = self._build_stop()
        self._send_templates = {value: self._build_send(value) for value in range(256)}
        self._read_ack = self._build_read(ack=True)
        self._read_nack = self._build_read(ack=False)
        self._configured = False

    # -- configuration -----------------------------------------------------
    def configure(self) -> None:
        """Synchronise with the MPSSE and configure it for I2C."""
        self._sync()
        buffer = bytearray(
            [
                DISABLE_CLOCK_DIV5,
                ENABLE_3_PHASE,
                SET_CLOCK_DIVISOR,
                self._divisor & 0xFF,
                (self._divisor >> 8) & 0xFF,
                DISABLE_LOOPBACK,
                # Open-drain on AD0/AD1/AD2: a '1' releases the line, a '0'
                # pulls it low. External pull-ups provide the high level.
                DRIVE_ZERO,
                0x07,
                0x00,
                SET_BITS_LOW,
                SDA_HIGH_SCL_HIGH,
                ADBUS_I2C_DIRECTION,
                ENABLE_ADAPTIVE_CLOCK if self.clock_stretching else DISABLE_ADAPTIVE_CLOCK,
            ]
        )
        self._transport.write(bytes(buffer))
        self._configured = True

    def _sync(self) -> None:
        self._transport.purge()
        self._transport.write(bytes([BAD_COMMAND]))
        response = self._transport.read(2)
        if response != bytes([BAD_COMMAND_ECHO, BAD_COMMAND]):
            raise I2cError(
                "FT232H: MPSSE did not echo the bad-command marker "
                f"(got {response.hex()}); check that the device is in MPSSE mode"
            )

    def _require_configured(self) -> None:
        if not self._configured:
            raise I2cError("FT232H: I2C engine is not configured (call configure() first)")

    # -- command templates -------------------------------------------------
    def _set_pins(self, value: int, repeat: int = 1) -> bytes:
        return bytes([SET_BITS_LOW, value, ADBUS_I2C_DIRECTION]) * repeat

    def _build_start(self) -> bytes:
        return (
            self._set_pins(SDA_HIGH_SCL_HIGH, self._setup_cycles)
            + self._set_pins(SDA_LOW_SCL_HIGH, self._setup_cycles)
            + self._set_pins(SDA_LOW_SCL_LOW, self._setup_cycles)
        )

    def _build_stop(self) -> bytes:
        return (
            self._set_pins(SDA_HIGH_SCL_LOW, self._setup_cycles)
            + self._set_pins(SDA_LOW_SCL_LOW, self._setup_cycles)
            + self._set_pins(SDA_LOW_SCL_HIGH, self._setup_cycles)
            + self._set_pins(SDA_HIGH_SCL_HIGH, self._setup_cycles)
        )

    def _build_send(self, value: int) -> bytes:
        # Clock out 8 bits, release SDA, then clock in the ACK/NACK bit.
        return (
            bytes([CLOCK_BYTES_OUT_POS_MSB, 0x00, 0x00, value & 0xFF])
            + self._set_pins(SDA_HIGH_SCL_LOW, self._nop_send)
            + bytes([CLOCK_BITS_IN_NEG_MSB, 0x00])
            + self._set_pins(SDA_HIGH_SCL_LOW, self._nop_send)
        )

    def _build_read(self, ack: bool) -> bytes:
        # Clock in 8 bits, then drive ACK (0x00) or NACK (0xFF) on the 9th bit.
        return (
            bytes([CLOCK_BYTES_IN_NEG_MSB, 0x00, 0x00])
            + bytes([CLOCK_BITS_OUT_POS_MSB, 0x00, 0x00 if ack else 0xFF])
            + self._set_pins(SDA_HIGH_SCL_LOW, self._nop_read)
        )

    # -- transactions ------------------------------------------------------
    @staticmethod
    def _check_address(address: int) -> None:
        if not 0 <= address <= 0x7F:
            raise ValueError(f"I2C address must be 7-bit (0x00-0x7F), got {address!r}")

    def _execute(self, command: bytes, expected: int) -> bytes:
        self._require_configured()
        self._transport.purge()
        self._transport.write(command)
        return self._transport.read(expected)

    def _check_acks(self, response: bytes, count: int, address: int) -> None:
        for index in range(count):
            if response[index] & 0x01:
                raise I2cNackError(
                    f"I2C NACK from 0x{address:02X} at byte {index} "
                    f"(response 0x{response[index]:02X})"
                )

    def write(self, address: int, data: Sequence[int]) -> None:
        """Write ``data`` to a 7-bit ``address`` (START, bytes, STOP)."""
        self._check_address(address)
        payload = bytes([(address << 1) & 0xFE, *(value & 0xFF for value in data)])
        command = bytearray(self._start_cmd)
        for value in payload:
            command += self._send_templates[value]
        command += self._stop_cmd
        command.append(SEND_IMMEDIATE)

        response = self._execute(bytes(command), len(payload))
        self._check_acks(response, len(payload), address)

    def read(self, address: int, prefix: Sequence[int] = (), count: int = 1) -> list[int]:
        """Read ``count`` bytes from a 7-bit ``address``.

        ``prefix`` bytes (usually one register address) are written first,
        followed by a repeated START and the read address.
        """
        self._check_address(address)
        if count < 1:
            raise ValueError("count must be at least 1")
        prefix = bytes(value & 0xFF for value in prefix)

        command = bytearray(self._start_cmd)
        command += self._send_templates[(address << 1) & 0xFE]
        for value in prefix:
            command += self._send_templates[value]
        command += self._start_cmd  # repeated START
        command += self._send_templates[(address << 1) | 0x01]
        for index in range(count):
            command += self._read_nack if index == count - 1 else self._read_ack
        command += self._stop_cmd
        command.append(SEND_IMMEDIATE)

        address_acks = 2 + len(prefix)
        response = self._execute(bytes(command), address_acks + count)
        self._check_acks(response, address_acks, address)
        return list(response[address_acks:])

    def write_register(self, address: int, register: int, data: Sequence[int] = (0,)) -> None:
        """Write ``data`` to an 8-bit ``register``."""
        if not 0 <= register <= 0xFF:
            raise ValueError(f"register must be 8-bit (0x00-0xFF), got {register!r}")
        self.write(address, [register, *(value & 0xFF for value in data)])

    def read_register(self, address: int, register: int, count: int = 1) -> list[int]:
        """Read ``count`` bytes starting at an 8-bit ``register``."""
        if not 0 <= register <= 0xFF:
            raise ValueError(f"register must be 8-bit (0x00-0xFF), got {register!r}")
        return self.read(address, [register], count)

    def probe(self, address: int) -> bool:
        """Return ``True`` when a device acknowledges ``address``."""
        self._check_address(address)
        command = bytearray(self._start_cmd)
        command += self._send_templates[(address << 1) & 0xFE]
        command += self._stop_cmd
        command.append(SEND_IMMEDIATE)
        response = self._execute(bytes(command), 1)
        return not response[0] & 0x01

    def scan(self, first: int = 0x08, last: int = 0x77) -> list[int]:
        """Return the sorted list of addresses that acknowledge a probe."""
        found = []
        for address in range(max(0, first), min(0x7F, last) + 1):
            try:
                if self.probe(address):
                    found.append(address)
            except I2cNackError:
                continue
        return found
