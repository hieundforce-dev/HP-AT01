"""Unit tests for the FT232H MPSSE I2C/GPIO engines (T04).

No FTDI hardware or D2XX library is needed: a fake transport records the MPSSE
commands and returns canned responses.
"""

from __future__ import annotations

import pytest
from hpat.drivers.ft232h_gpio import MpsseGpio
from hpat.drivers.ft232h_i2c import I2cError, I2cNackError, MpsseI2C
from hpat.drivers.ft232h_mpsse import clock_divisor

SYNC = b"\xfa\xaa"


class FakeTransport:
    """Record writes and replay a fixed response buffer."""

    def __init__(self, response: bytes = b"") -> None:
        self.writes: list[bytes] = []
        self.response = bytearray(response)
        self.purges = 0

    def write(self, data: bytes) -> int:
        self.writes.append(bytes(data))
        return len(data)

    def read(self, size: int) -> bytes:
        if len(self.response) < size:
            raise AssertionError(
                f"fake transport has {len(self.response)} byte(s), read requested {size}"
            )
        chunk = bytes(self.response[:size])
        del self.response[:size]
        return chunk

    def purge(self) -> None:
        self.purges += 1


def make_engine(response: bytes = b"", **kwargs: object) -> tuple[MpsseI2C, FakeTransport]:
    transport = FakeTransport(SYNC + response)
    engine = MpsseI2C(transport, **kwargs)
    engine.configure()
    return engine, transport


def test_clock_divisor_for_common_rates() -> None:
    assert clock_divisor(100_000) == 299
    assert clock_divisor(400_000) == 74
    assert clock_divisor(1_000_000) == 29


def test_clock_divisor_is_clamped_and_validated() -> None:
    assert clock_divisor(50_000_000) == 0
    assert clock_divisor(1) == 0xFFFF
    with pytest.raises(ValueError):
        clock_divisor(0)


def test_configure_sends_expected_mpss_e_sequence() -> None:
    _, transport = make_engine()

    assert transport.writes[0] == b"\xaa"
    config = transport.writes[1]
    assert 0x8A in config  # 60 MHz base clock
    assert 0x8C in config  # 3-phase clocking
    assert 0x9E in config  # Drive-Zero / open-drain
    assert config[config.index(0x86) + 1 : config.index(0x86) + 3] == bytes([0x2B, 0x01])
    assert 0x97 in config  # adaptive clocking disabled by default


def test_configure_enables_clock_stretching() -> None:
    _, transport = make_engine(clock_stretching=True)

    assert 0x96 in transport.writes[1]


def test_write_builds_start_address_data_stop() -> None:
    engine, transport = make_engine(b"\x00\x00\x00")

    engine.write(0x50, [0x10, 0xAB])
    command = transport.writes[-1]

    assert command.startswith(engine._start_cmd)
    assert bytes([0x11, 0x00, 0x00, 0xA0]) in command  # address + write
    assert bytes([0x11, 0x00, 0x00, 0x10]) in command  # register
    assert bytes([0x11, 0x00, 0x00, 0xAB]) in command  # data
    assert command.endswith(engine._stop_cmd + b"\x87")
    assert command.count(engine._start_cmd) == 1


def test_write_register_is_a_single_transaction() -> None:
    engine, transport = make_engine(b"\x00\x00\x00")

    engine.write_register(0x21, 0x0F, [0x55])
    command = transport.writes[-1]

    assert command.count(engine._start_cmd) == 1
    assert bytes([0x11, 0x00, 0x00, 0x42]) in command
    assert bytes([0x11, 0x00, 0x00, 0x0F]) in command
    assert bytes([0x11, 0x00, 0x00, 0x55]) in command


def test_write_raises_on_nack() -> None:
    engine, _ = make_engine(b"\x01\x00\x00")

    with pytest.raises(I2cNackError, match="NACK from 0x50"):
        engine.write(0x50, [0x00, 0xAA])


def test_read_uses_repeated_start_and_returns_data() -> None:
    engine, transport = make_engine(b"\x00\x00\x00\x12\x34")

    data = engine.read_register(0x50, 0x00, count=2)
    command = transport.writes[-1]

    assert data == [0x12, 0x34]
    assert command.count(engine._start_cmd) == 2
    assert bytes([0x11, 0x00, 0x00, 0xA1]) in command  # address + read
    assert bytes([0x13, 0x00, 0x00]) in command  # ACK for the first byte
    assert bytes([0x13, 0x00, 0xFF]) in command  # NACK for the last byte


def test_read_raises_on_address_nack() -> None:
    engine, _ = make_engine(b"\x00\x01\x00\x00")

    with pytest.raises(I2cNackError, match="byte 1"):
        engine.read_register(0x50, 0x00)


def test_scan_reports_only_acknowledging_addresses() -> None:
    class ScanTransport(FakeTransport):
        def __init__(self) -> None:
            super().__init__(SYNC)
            self.present = {0x20, 0x50}

        def read(self, size: int) -> bytes:
            if size == 2 and self.writes[-1] == b"\xaa":
                return SYNC
            command = self.writes[-1]
            marker = command.index(bytes([0x11, 0x00, 0x00]))
            wire_address = command[marker + 3]
            return b"\x00" if (wire_address >> 1) in self.present else b"\x01"

    transport = ScanTransport()
    engine = MpsseI2C(transport)
    engine.configure()

    assert engine.scan(0x10, 0x60) == [0x20, 0x50]


def test_address_and_register_validation() -> None:
    engine, _ = make_engine()

    with pytest.raises(ValueError, match="7-bit"):
        engine.write(0x80, [0x00])
    with pytest.raises(ValueError, match="8-bit"):
        engine.read_register(0x50, 0x100)
    with pytest.raises(ValueError, match="at least 1"):
        engine.read(0x50, count=0)


def test_engine_requires_configure() -> None:
    engine = MpsseI2C(FakeTransport())

    with pytest.raises(I2cError, match="not configured"):
        engine.write(0x50, [0x00])


def test_gpio_starts_as_inputs_and_can_drive_a_pin() -> None:
    transport = FakeTransport()
    gpio = MpsseGpio(transport)

    gpio.configure()
    assert transport.writes[-1] == bytes([0x82, 0x00, 0x00])

    gpio.write(3, True)
    assert transport.writes[-1] == bytes([0x82, 0x08, 0x08])

    gpio.set_direction(3, False)
    assert transport.writes[-1] == bytes([0x82, 0x08, 0x00])


def test_gpio_read_returns_pin_level() -> None:
    transport = FakeTransport(b"\x05\x05\x05")
    gpio = MpsseGpio(transport)
    gpio.configure()

    assert gpio.read(0) is True
    assert gpio.read(1) is False
    assert gpio.read(2) is True


def test_gpio_read_all() -> None:
    transport = FakeTransport(b"\xa5")
    gpio = MpsseGpio(transport)
    gpio.configure()

    assert gpio.read_all() == 0xA5


def test_gpio_rejects_invalid_pin() -> None:
    gpio = MpsseGpio(FakeTransport())

    with pytest.raises(ValueError, match="0-7"):
        gpio.write(8, True)
