"""Simulated instruments used when ``simulation: true`` or ``hpat sim``.

They implement the same interface as the real drivers, keep a small amount of
state (setpoints, output on/off) and answer the SCPI queries the test items
use. This lets the whole pipeline run without a bench.
"""

from __future__ import annotations

import re
from typing import Any

from hpat.drivers.base import Instrument

_CHANNEL_CMD = re.compile(r"^(VSET|ISET|OUT)(\d):?(.*)$")


class SimInstrument(Instrument):
    """Common simulated behaviour: state tracking and command history."""

    model = "SIM"

    def __init__(self, role: str, config: Any) -> None:
        super().__init__(role, config)
        self.is_open = False
        self.commands: list[str] = []

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    def identify(self) -> str:
        return f"SIM,{self.model},SN000000,FW0.0"

    def write(self, command: str) -> None:
        self.commands.append(command)
        self._handle(command)

    def query(self, command: str) -> str:
        self.commands.append(command)
        return self._answer(command)

    def query_float(self, command: str) -> float:
        return float(self.query(command))

    def _handle(self, command: str) -> None:  # pragma: no cover - overridden
        """Apply a write command to the simulated state."""

    def _answer(self, command: str) -> str:
        if command.strip() == "*IDN?":
            return self.identify()
        return "OK"


class SimPsu(SimInstrument):
    """GW Instek GPD-3303S: two channels, voltage/current setpoints, output."""

    model = "GW INSTEK,GPD-3303S"

    def __init__(self, role: str, config: Any) -> None:
        super().__init__(role, config)
        self.voltage: dict[int, float] = {1: 0.0, 2: 0.0}
        self.current: dict[int, float] = {1: 0.0, 2: 0.0}
        self.output: dict[int, bool] = {1: False, 2: False}

    def _handle(self, command: str) -> None:
        match = _CHANNEL_CMD.match(command.strip().upper())
        if not match:
            return
        action, channel_text, argument = match.groups()
        channel = int(channel_text)
        if action == "VSET" and argument:
            self.voltage[channel] = float(argument)
        elif action == "ISET" and argument:
            self.current[channel] = float(argument)
        elif action == "OUT":
            if argument:
                self.output[channel] = argument == "1"
            elif channel == 0:
                self.output = {1: False, 2: False}
            else:
                self.output = {1: True, 2: True}

    def _answer(self, command: str) -> str:
        cmd = command.strip().upper()
        if cmd.startswith("VOUT") and cmd.endswith("?"):
            return f"{self._read(self.voltage, cmd[4]):.3f}"
        if cmd.startswith("IOUT") and cmd.endswith("?"):
            return f"{self._read(self.current, cmd[4]):.3f}"
        return super()._answer(command)

    def _read(self, values: dict[int, float], channel_text: str) -> float:
        channel = int(channel_text)
        return values[channel] if self.output[channel] else 0.0


class SimEload(SimInstrument):
    """3315D electronic load: CC/CV/CR/CP mode, setpoint, input on/off."""

    model = "3315D,DC ELECTRONIC LOAD"

    def __init__(self, role: str, config: Any) -> None:
        super().__init__(role, config)
        self.mode = "CC"
        self.level = 0.0
        self.input_on = False
        self.measured_voltage = 12.0

    def _handle(self, command: str) -> None:
        parts = command.strip().upper().split()
        if len(parts) == 2 and parts[0] == "MODE":
            self.mode = parts[1]
        elif len(parts) == 2 and parts[0] in {"CURR", "VOLT", "RES", "POW"}:
            self.level = float(parts[1])
        elif len(parts) == 2 and parts[0] == "INP":
            self.input_on = parts[1] == "ON"
        elif parts == ["INP", "1"]:
            self.input_on = True

    def _answer(self, command: str) -> str:
        cmd = command.strip().upper()
        if cmd == "MEAS:CURR?":
            return f"{self.level if self.input_on else 0.0:.3f}"
        if cmd == "MEAS:VOLT?":
            return f"{self.measured_voltage if self.input_on else 0.0:.3f}"
        if cmd == "MODE?":
            return self.mode
        return super()._answer(command)


class SimScope(SimInstrument):
    """Tektronix TBS2204B: channel selection and basic measurements."""

    model = "TEKTRONIX,TBS2204B"

    def __init__(self, role: str, config: Any) -> None:
        super().__init__(role, config)
        self.selected_channel = 1
        self.measurements: dict[tuple[str, int], float] = {}

    def _handle(self, command: str) -> None:
        cmd = command.strip().upper()
        if cmd.startswith("SEL:CH"):
            self.selected_channel = int(cmd[6:])
        elif cmd.startswith("DAT:SOU") and "CH" in cmd:
            self.selected_channel = int(cmd.split("CH")[-1])

    def _answer(self, command: str) -> str:
        cmd = command.strip().upper()
        match = re.match(r"MEASU:(?:CH(\d):)?(VPP|VRMS|FREQ|MEAN)\?", cmd)
        if match:
            channel = int(match.group(1)) if match.group(1) else self.selected_channel
            return f"{self.measurements.get((match.group(2), channel), 0.012):.6f}"
        return super()._answer(command)


class SimDmm(SimInstrument):
    """Bench multimeter: DC voltage / DC current measurements."""

    model = "UNI-T,UT8805E"
    default_voltage = 12.0
    default_current = 0.5

    def __init__(self, role: str, config: Any) -> None:
        super().__init__(role, config)
        self.voltage = self.default_voltage
        self.current = self.default_current

    def _answer(self, command: str) -> str:
        cmd = command.strip().upper()
        if cmd.startswith("MEAS:VOLT") or cmd.startswith("CONF:VOLT"):
            return f"{self.voltage:.6f}"
        if cmd.startswith("MEAS:CURR") or cmd.startswith("CONF:CURR"):
            return f"{self.current:.6f}"
        if cmd == "READ?":
            return f"{self.voltage:.6f}"
        return super()._answer(command)


class SimUt8805E(SimDmm):
    model = "UNI-T,UT8805E"


class SimKeithley2000(SimDmm):
    model = "KEITHLEY,MODEL 2000"


class SimKeithley2100(SimDmm):
    model = "KEITHLEY,MODEL 2100"


class SimFt232h(SimInstrument):
    """FT232H bridge: I2C and GPIO over MPSSE (simulated register file)."""

    model = "FTDI,FT232H"

    def __init__(self, role: str, config: Any) -> None:
        super().__init__(role, config)
        self.registers: dict[int, int] = {}
        self.gpio_state: int = 0

    def i2c_write(self, address: int, register: int, value: int) -> None:
        self.registers[register] = value & 0xFF

    def i2c_read(self, address: int, register: int) -> int:
        return self.registers.get(register, 0)

    def set_gpio(self, pin: int, level: bool) -> None:
        if level:
            self.gpio_state |= 1 << pin
        else:
            self.gpio_state &= ~(1 << pin)

    def read_gpio(self, pin: int) -> bool:
        return bool(self.gpio_state & (1 << pin))
