"""Low-level MPSSE transport and opcodes for the FT232H (T04).

Only the FT232H is supported. The I2C wiring is the one used by the
MIT-licensed reference implementation ``cyangy/ftdi_mpsse_python`` and by
pyftdi, and verified on the project bench:

======  =========================  ==========================================
Pin     Signal                     Notes
======  =========================  ==========================================
ADBUS0  SCL                        open-drain (Drive-Zero), external pull-up
ADBUS1  SDA (drive)                open-drain (Drive-Zero)
ADBUS2  SDA (sense)                tie ADBUS1 and ADBUS2 together at the DUT
GND     GND
======  =========================  ==========================================

External 2.2k-10k pull-ups to 3.3 V are required on SCL and SDA. ACBUS0-7 are
left free for GPIO (see :mod:`hpat.drivers.ft232h_gpio`).

Opcode values come from FTDI AN_108 and were checked against the reference
implementation; the naming below follows AN_108.
"""

from __future__ import annotations

import time
from typing import Any, Protocol

from hpat.core.errors import InstrumentError

#: ``FT_DEVICE_232H`` in the D2XX API (``ftd2xx.defines.DEVICE_232H``).
FTDI_DEVICE_232H = 8

# --- MPSSE opcodes (AN_108) -------------------------------------------------
CLOCK_BYTES_OUT_POS_MSB = 0x11  # clock out bytes, MSB first, data changes on -ve
CLOCK_BITS_OUT_POS_MSB = 0x13  # clock out bits, MSB first
CLOCK_BYTES_IN_NEG_MSB = 0x20  # clock in bytes, MSB first
CLOCK_BITS_IN_NEG_MSB = 0x22  # clock in bits, MSB first

SET_BITS_LOW = 0x80
SET_BITS_HIGH = 0x82
READ_BITS_LOW = 0x81
READ_BITS_HIGH = 0x83

DISABLE_CLOCK_DIV5 = 0x8A
ENABLE_CLOCK_DIV5 = 0x8B
ENABLE_3_PHASE = 0x8C
DISABLE_3_PHASE = 0x8D
ENABLE_ADAPTIVE_CLOCK = 0x96
DISABLE_ADAPTIVE_CLOCK = 0x97
SET_CLOCK_DIVISOR = 0x86
DRIVE_ZERO = 0x9E
DISABLE_LOOPBACK = 0x85
SEND_IMMEDIATE = 0x87

BAD_COMMAND = 0xAA
BAD_COMMAND_ECHO = 0xFA

# --- ADBUS pin values/directions for I2C ------------------------------------
SDA_HIGH_SCL_HIGH = 0x03
SDA_LOW_SCL_HIGH = 0x01
SDA_LOW_SCL_LOW = 0x00
SDA_HIGH_SCL_LOW = 0x02
ADBUS_I2C_DIRECTION = 0x03  # AD0/AD1 outputs, AD2.. inputs

#: FT232H MPSSE base clock after ``DISABLE_CLOCK_DIV5``.
MPSSE_BASE_CLOCK_HZ = 60_000_000


class MpsseError(InstrumentError):
    """Low-level MPSSE/FTDI failure."""


class MpsseTimeout(MpsseError):
    """The FT232H did not return the expected number of bytes in time."""


class Transport(Protocol):
    """Minimal transport used by the I2C/GPIO engines (easy to fake in tests)."""

    def write(self, data: bytes) -> int:
        """Send raw MPSSE commands, return the number of bytes accepted."""

    def read(self, size: int) -> bytes:
        """Read exactly ``size`` bytes of MPSSE responses."""

    def purge(self) -> None:
        """Discard pending USB buffers."""


class FtdiTransport:
    """Wrap a ``ftd2xx`` device in the small transport interface."""

    def __init__(self, device: Any, timeout_s: float = 2.0) -> None:
        self._device = device
        self._timeout_s = timeout_s

    def write(self, data: bytes) -> int:
        try:
            written = int(self._device.write(bytes(data)))
        except Exception as exc:  # pragma: no cover - hardware path
            raise MpsseError(f"FT232H: USB write failed: {exc}") from exc
        if written != len(data):
            raise MpsseError(
                f"FT232H: short USB write ({written}/{len(data)} bytes); "
                "check the USB cable and that no other program owns the device"
            )
        return written

    def read(self, size: int) -> bytes:
        if size <= 0:
            return b""
        deadline = time.monotonic() + self._timeout_s
        buffer = bytearray()
        while len(buffer) < size:
            try:
                chunk = bytes(self._device.read(size - len(buffer)))
            except Exception as exc:  # pragma: no cover - hardware path
                raise MpsseError(f"FT232H: USB read failed: {exc}") from exc
            buffer.extend(chunk)
            if len(buffer) >= size:
                break
            if time.monotonic() >= deadline:
                raise MpsseTimeout(
                    f"FT232H: timed out waiting for {size} byte(s), got {len(buffer)}; "
                    "is the MPSSE wired correctly?"
                )
            time.sleep(0.001)
        return bytes(buffer)

    def purge(self) -> None:
        try:
            self._device.purge()
        except Exception as exc:  # pragma: no cover - hardware path
            raise MpsseError(f"FT232H: cannot purge USB buffers: {exc}") from exc


def clock_divisor(clock_hz: float) -> int:
    """Return the MPSSE divisor for ``clock_hz`` with 3-phase clocking.

    ``f = 60 MHz / (2 * (1 + divisor))``; the result is clamped to the 16-bit
    register range. The real SCL frequency is approximately the requested one.
    """
    if clock_hz <= 0:
        raise ValueError("clock_hz must be positive")
    divisor = round(MPSSE_BASE_CLOCK_HZ / (2 * clock_hz)) - 1
    return max(0, min(divisor, 0xFFFF))


def _import_ftd2xx() -> Any:
    try:
        import ftd2xx
    except Exception as exc:
        raise MpsseError(
            "FT232H: D2XX library not available. Install the FTDI D2XX driver "
            "(CDM) and libftd2xx, remove VCP binding for the FT232H, then retry "
            "(see docs/USER_MANUAL.md)."
        ) from exc
    return ftd2xx


def _text(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("ascii", errors="replace").strip("\x00 ")
    return str(value).strip() if value is not None else ""


def ft232h_label(device: Any) -> str:
    """Build an identification string from a D2XX device."""
    info = device.getDeviceInfo()
    description = _text(info.get("description")) or "FT232H"
    serial = _text(info.get("serial"))
    return f"FTDI,{description},SN{serial}" if serial else f"FTDI,{description}"


def open_ft232h(serial: str = "", index: int = 0, timeout_s: float = 2.0) -> Any:
    """Open and initialise an FT232H in MPSSE mode.

    Args:
        serial: D2XX serial number. When empty, ``index`` is used.
        index: Device index in ``ftd2xx.listDevices()``.
        timeout_s: Read timeout used by the transport.

    Raises:
        MpsseError: D2XX is missing, the device is not an FT232H, or the
            MPSSE could not be enabled.
    """
    ftd2xx = _import_ftd2xx()
    try:
        devices = ftd2xx.listDevices()
    except Exception as exc:  # pragma: no cover - hardware path
        raise MpsseError(f"FT232H: cannot enumerate D2XX devices: {exc}") from exc
    if not devices:
        raise MpsseError(
            "FT232H: no D2XX device found. Plug the FT232H, install the D2XX "
            "driver and remove the VCP binding (see docs/USER_MANUAL.md)."
        )

    try:
        if serial:
            device = ftd2xx.openEx(serial.encode("ascii"))
        else:
            if not 0 <= index < len(devices):
                raise MpsseError(
                    f"FT232H: device index {index} out of range "
                    f"({len(devices)} D2XX device(s) found)"
                )
            device = ftd2xx.open(index)
    except MpsseError:
        raise
    except Exception as exc:  # pragma: no cover - hardware path
        raise MpsseError(f"FT232H: cannot open D2XX device: {exc}") from exc

    try:
        info = device.getDeviceInfo()
        device_type = int(info.get("type", -1))
        if device_type != FTDI_DEVICE_232H:
            raise MpsseError(
                f"FT232H: unsupported FTDI device type {device_type} (only the FT232H is supported)"
            )
        device.setBitMode(0x00, 0x00)  # reset
        time.sleep(0.05)
        device.setBitMode(0x00, 0x02)  # MPSSE
        device.setTimeouts(50, int(timeout_s * 1000))
        device.purge()
    except Exception:
        device.close()
        raise
    return device
