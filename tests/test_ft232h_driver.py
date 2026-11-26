"""Tests for the FT232H instrument driver (T04), without hardware."""

from __future__ import annotations

import pytest
from hpat.core.config import InstrumentConfig
from hpat.core.errors import InstrumentError
from hpat.drivers import ft232h_driver
from hpat.drivers.ft232h_driver import Ft232hDriver
from hpat.drivers.ft232h_mpsse import MpsseError

SYNC = b"\xfa\xaa"


class FakeTransport:
    def __init__(self, response: bytes = b"") -> None:
        self.writes: list[bytes] = []
        self.response = bytearray(response)
        self.purges = 0

    def write(self, data: bytes) -> int:
        self.writes.append(bytes(data))
        return len(data)

    def read(self, size: int) -> bytes:
        if len(self.response) < size:
            raise AssertionError(f"need {size} byte(s), have {len(self.response)}")
        chunk = bytes(self.response[:size])
        del self.response[:size]
        return chunk

    def purge(self) -> None:
        self.purges += 1


def make_config(**options: object) -> InstrumentConfig:
    return InstrumentConfig(driver="ft232h", resource="FT232H-A", options=options)


def test_driver_roundtrip_with_injected_transport() -> None:
    transport = FakeTransport(SYNC + b"\x00\x00\x00" + b"\x00\x00\x00\x2a" + b"\x05")
    driver = Ft232hDriver("ft232h", make_config(), transport=transport)

    driver.open()
    assert driver.identify() == "FTDI,FT232H,INJECTED"

    driver.i2c_write(0x50, 0x10, 0xAB)
    assert driver.i2c_read(0x50, 0x10) == 0x2A

    driver.set_gpio(0, True)
    assert driver.read_gpio(2) is True

    driver.close()
    driver.close()  # idempotent
    with pytest.raises(InstrumentError, match="not open"):
        driver.i2c_read(0x50, 0x10)


def test_driver_configures_requested_clock() -> None:
    transport = FakeTransport(SYNC)
    driver = Ft232hDriver("ft232h", make_config(i2c_frequency_hz=400_000), transport=transport)

    driver.open()

    config = transport.writes[1]
    assert config[config.index(0x86) + 1 : config.index(0x86) + 3] == bytes([0x4A, 0x00])
    driver.close()


def test_driver_open_reports_missing_d2xx(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(**_kwargs: object) -> None:
        raise MpsseError("FT232H: D2XX library not available")

    monkeypatch.setattr(ft232h_driver, "open_ft232h", fail)
    driver = Ft232hDriver("ft232h", make_config())

    with pytest.raises(MpsseError, match="D2XX library not available"):
        driver.open()
    driver.close()


def test_driver_rejects_bad_address_and_pin() -> None:
    transport = FakeTransport(SYNC)
    driver = Ft232hDriver("ft232h", make_config(), transport=transport)
    driver.open()

    with pytest.raises(ValueError, match="7-bit"):
        driver.i2c_write(0x80, 0x00, 0x00)
    with pytest.raises(ValueError, match="0-7"):
        driver.set_gpio(8, True)

    driver.close()


def test_driver_rejects_non_numeric_option() -> None:
    driver = Ft232hDriver("ft232h", make_config(i2c_frequency_hz="fast"), transport=FakeTransport())

    with pytest.raises(InstrumentError, match="must be a number"):
        driver.open()
