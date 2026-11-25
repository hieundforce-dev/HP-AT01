"""Instrument configuration loaded from ``config/instruments.yaml``.

The file describes which driver talks to which VISA resource and the safety
limits that must never be exceeded. All values are validated up front so the
bench is never opened with a broken configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from hpat.core.errors import ConfigError

#: Instrument roles the rest of the application looks up by name.
REQUIRED_ROLES = ("psu", "eload", "scope", "ft232h")
OPTIONAL_ROLES = ("dmm_vin", "dmm_vout", "dmm_iout")
ALLOWED_ROLES = REQUIRED_ROLES + OPTIONAL_ROLES


class InstrumentConfig(BaseModel):
    """One physical instrument: driver name, VISA resource and driver options."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    driver: str = Field(min_length=1, description="Driver module name, e.g. gwinstek_gpd3303s.")
    resource: str = Field(default="", description="VISA resource string or FTDI serial.")
    options: dict[str, Any] = Field(
        default_factory=dict,
        description="Driver specific options (channel, gpib_address, shunt_ohm, ...).",
    )


class SafetyConfig(BaseModel):
    """Hard limits applied before any command is sent to the bench."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    max_voltage_v: float = Field(gt=0, description="Highest voltage allowed on any rail.")
    max_current_a: float = Field(gt=0, description="Highest current allowed on any rail.")
    max_power_w: float | None = Field(default=None, gt=0)
    settle_ms_default: int = Field(default=200, ge=0)
    power_up_order: list[str] = Field(default_factory=lambda: ["psu", "eload"])
    power_down_order: list[str] = Field(default_factory=lambda: ["eload", "psu"])

    @model_validator(mode="after")
    def _check_order_roles(self) -> SafetyConfig:
        for label, order in (
            ("power_up_order", self.power_up_order),
            ("power_down_order", self.power_down_order),
        ):
            unknown = [role for role in order if role not in ALLOWED_ROLES]
            if unknown:
                raise ValueError(f"{label} contains unknown roles: {', '.join(unknown)}")
        return self


class BenchConfig(BaseModel):
    """Whole bench configuration."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    simulation: bool = False
    instruments: dict[str, InstrumentConfig]
    safety: SafetyConfig

    @model_validator(mode="after")
    def _check_roles(self) -> BenchConfig:
        unknown = [role for role in self.instruments if role not in ALLOWED_ROLES]
        if unknown:
            raise ValueError(
                "unknown instrument roles: "
                + ", ".join(sorted(unknown))
                + f" (allowed: {', '.join(ALLOWED_ROLES)})"
            )
        missing = [role for role in REQUIRED_ROLES if role not in self.instruments]
        if missing:
            raise ValueError(f"missing required instrument roles: {', '.join(missing)}")
        return self

    def instrument(self, role: str) -> InstrumentConfig:
        """Return the configuration of ``role`` or raise a clear error."""
        try:
            return self.instruments[role]
        except KeyError as exc:
            raise ConfigError(f"Instrument role '{role}' is not configured.") from exc


def _format_validation_error(exc: ValidationError, path: Path) -> ConfigError:
    lines = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"]) or "<root>"
        lines.append(f"  - {location}: {error['msg']}")
    return ConfigError(f"Invalid config '{path}':\n" + "\n".join(lines))


def load_config(path: Path | str) -> BenchConfig:
    """Load and validate the instrument configuration.

    Raises:
        ConfigError: the file is missing, is not valid YAML, or fails validation.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" (line {mark.line + 1}, column {mark.column + 1})" if mark else ""
        raise ConfigError(f"Invalid YAML in '{config_path}'{where}: {exc}") from exc

    if raw is None:
        raise ConfigError(f"Config file is empty: {config_path}")
    if not isinstance(raw, dict):
        raise ConfigError(f"Config file must contain a mapping at the top level: {config_path}")

    try:
        return BenchConfig.model_validate(raw)
    except ValidationError as exc:
        raise _format_validation_error(exc, config_path) from exc
