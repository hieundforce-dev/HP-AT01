"""Base classes for instrument drivers.

A driver exposes a small, explicit API (``open``/``close``/``identify``) and,
for VISA instruments, ``write``/``query`` with retry and SCPI logging.
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from types import TracebackType
from typing import Any

from hpat.core.config import InstrumentConfig
from hpat.core.errors import InstrumentError

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_MS = 5000
DEFAULT_RETRIES = 2
DEFAULT_RETRY_DELAY_S = 0.2


class Instrument(ABC):
    """Common interface every driver implements."""

    def __init__(self, role: str, config: InstrumentConfig) -> None:
        self.role = role
        self.config = config

    @abstractmethod
    def open(self) -> None:
        """Connect to the instrument."""

    @abstractmethod
    def close(self) -> None:
        """Release the connection. Must be safe to call twice."""

    @abstractmethod
    def identify(self) -> str:
        """Return an identification string (``*IDN?`` or equivalent)."""

    def __enter__(self) -> Instrument:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


class VisaInstrument(Instrument):
    """Instrument reached through a PyVISA resource.

    The VISA resource is opened lazily in :meth:`open` so that constructing a
    driver never touches the bench. A pre-opened resource may be injected for
    tests.
    """

    def __init__(
        self,
        role: str,
        config: InstrumentConfig,
        resource_obj: Any | None = None,
        retries: int = DEFAULT_RETRIES,
        retry_delay_s: float = DEFAULT_RETRY_DELAY_S,
    ) -> None:
        super().__init__(role, config)
        self._resource = resource_obj
        self._retries = retries
        self._retry_delay_s = retry_delay_s

    @property
    def resource(self) -> Any | None:
        return self._resource

    def open(self) -> None:
        if self._resource is not None:
            return
        if not self.config.resource:
            raise InstrumentError(f"{self.role}: no VISA resource configured")
        try:
            import pyvisa
        except ImportError as exc:  # pragma: no cover - pyvisa is a hard dependency
            raise InstrumentError(f"{self.role}: pyvisa is not installed") from exc

        try:
            manager = pyvisa.ResourceManager()
            self._resource = manager.open_resource(self.config.resource)
            timeout = int(self.config.options.get("timeout_ms", DEFAULT_TIMEOUT_MS))
            self._resource.timeout = timeout
        except Exception as exc:
            raise InstrumentError(
                f"{self.role}: cannot open VISA resource '{self.config.resource}': {exc}"
            ) from exc

    def close(self) -> None:
        if self._resource is None:
            return
        try:
            self._resource.close()
        except Exception as exc:  # closing must never mask the original error
            logger.warning("%s: error while closing resource: %s", self.role, exc)
        finally:
            self._resource = None

    def identify(self) -> str:
        return self.query("*IDN?")

    def write(self, command: str) -> None:
        self._require_open()
        logger.debug("%s TX %r", self.role, command)

        def action() -> None:
            self._resource.write(command)

        self._with_retry(action, f"write {command!r}")

    def query(self, command: str) -> str:
        self._require_open()
        logger.debug("%s TX %r", self.role, command)

        def action() -> str:
            return str(self._resource.query(command)).strip()

        response = self._with_retry(action, f"query {command!r}")
        logger.debug("%s RX %r", self.role, response)
        return response

    def query_float(self, command: str) -> float:
        """Query a numeric value, raising a clear error on malformed answers."""
        response = self.query(command)
        try:
            return float(response)
        except ValueError as exc:
            raise InstrumentError(
                f"{self.role}: expected a number from {command!r}, got {response!r}"
            ) from exc

    def _require_open(self) -> None:
        if self._resource is None:
            raise InstrumentError(f"{self.role}: instrument is not open")

    def _with_retry(self, action: Callable[[], Any], description: str) -> Any:
        attempts = self._retries + 1
        last_error: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                return action()
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "%s: %s failed (attempt %d/%d): %s",
                    self.role,
                    description,
                    attempt,
                    attempts,
                    exc,
                )
                if attempt < attempts:
                    time.sleep(self._retry_delay_s)
        raise InstrumentError(
            f"{self.role}: {description} failed after {attempts} attempts: {last_error}"
        ) from last_error
