"""Tests for the VISA driver base (T03)."""

from __future__ import annotations

import logging
from typing import Any

import pytest
from hpat.core.config import InstrumentConfig
from hpat.core.errors import InstrumentError
from hpat.drivers.base import VisaInstrument


class FakeResource:
    """Minimal PyVISA resource double."""

    def __init__(
        self,
        responses: dict[str, str] | None = None,
        fail_query_times: int = 0,
        fail_write_times: int = 0,
        close_error: Exception | None = None,
    ) -> None:
        self.responses = responses or {}
        self.fail_query_times = fail_query_times
        self.fail_write_times = fail_write_times
        self.close_error = close_error
        self.writes: list[str] = []
        self.queries: list[str] = []
        self.timeout: int | None = None
        self.closed = False

    def write(self, command: str) -> None:
        if self.fail_write_times > 0:
            self.fail_write_times -= 1
            raise RuntimeError("write failed")
        self.writes.append(command)

    def query(self, command: str) -> str:
        if self.fail_query_times > 0:
            self.fail_query_times -= 1
            raise RuntimeError("query failed")
        self.queries.append(command)
        return self.responses.get(command, "OK\n")

    def close(self) -> None:
        self.closed = True
        if self.close_error is not None:
            raise self.close_error


class ListHandler(logging.Handler):
    """Collect formatted log messages for assertions."""

    def __init__(self) -> None:
        super().__init__()
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.messages.append(record.getMessage())


def make_instrument(resource: Any, **kwargs: Any) -> VisaInstrument:
    config = InstrumentConfig(driver="fake", resource="FAKE::INSTR")
    return VisaInstrument("psu", config, resource_obj=resource, retry_delay_s=0, **kwargs)


def test_identify_strips_response() -> None:
    resource = FakeResource(responses={"*IDN?": "GW INSTEK,GPD-3303S,SN1,FW1\n"})
    assert make_instrument(resource).identify() == "GW INSTEK,GPD-3303S,SN1,FW1"


def test_write_and_query_are_logged_at_debug() -> None:
    resource = FakeResource(responses={"VOUT1?": "12.000\n"})
    instrument = make_instrument(resource)

    logger = logging.getLogger("hpat.drivers.base")
    handler = ListHandler()
    previous_level = logger.level
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:
        instrument.write("VSET1:12.00")
        assert instrument.query("VOUT1?") == "12.000"
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)

    assert any("TX 'VSET1:12.00'" in message for message in handler.messages)
    assert any("RX '12.000'" in message for message in handler.messages)


def test_query_retries_then_succeeds() -> None:
    resource = FakeResource(responses={"*IDN?": "IDN\n"}, fail_query_times=1)
    assert make_instrument(resource, retries=2).identify() == "IDN"
    assert resource.queries == ["*IDN?"]


def test_query_failure_is_wrapped_with_context() -> None:
    resource = FakeResource(fail_query_times=10)
    with pytest.raises(InstrumentError) as excinfo:
        make_instrument(resource, retries=1).query("*IDN?")

    message = str(excinfo.value)
    assert "psu" in message
    assert "query '*IDN?'" in message
    assert "2 attempts" in message


def test_write_failure_is_wrapped() -> None:
    resource = FakeResource(fail_write_times=10)
    with pytest.raises(InstrumentError, match="write 'OUT1'"):
        make_instrument(resource, retries=0).write("OUT1")


def test_operations_require_open() -> None:
    config = InstrumentConfig(driver="fake", resource="FAKE::INSTR")
    instrument = VisaInstrument("psu", config)
    with pytest.raises(InstrumentError, match="not open"):
        instrument.write("OUT1")


def test_open_without_resource_is_reported() -> None:
    config = InstrumentConfig(driver="fake", resource="")
    with pytest.raises(InstrumentError, match="no VISA resource configured"):
        VisaInstrument("psu", config).open()


def test_query_float_parses_and_validates() -> None:
    resource = FakeResource(responses={"VOUT1?": "12.345\n", "IOUT1?": "not-a-number\n"})
    instrument = make_instrument(resource)

    assert instrument.query_float("VOUT1?") == pytest.approx(12.345)
    with pytest.raises(InstrumentError, match="expected a number"):
        instrument.query_float("IOUT1?")


def test_close_is_idempotent_and_swallows_errors() -> None:
    resource = FakeResource(close_error=RuntimeError("bus error"))
    instrument = make_instrument(resource)

    instrument.close()
    instrument.close()

    assert resource.closed is True
