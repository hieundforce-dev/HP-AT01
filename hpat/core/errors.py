"""Exception hierarchy for HP-AT01.

Every error raised by the application derives from :class:`HpatError` so the
CLI can print a friendly message instead of a traceback.
"""

from __future__ import annotations


class HpatError(Exception):
    """Base class for all HP-AT01 errors."""


class ConfigError(HpatError):
    """Instrument configuration is missing or invalid."""


class PlanError(HpatError):
    """A test plan file is missing, malformed, or fails schema validation."""


class InstrumentError(HpatError):
    """An instrument could not be opened or did not answer as expected."""


class SafetyError(HpatError):
    """A requested setting would violate a safety limit; nothing was applied."""


class TestAborted(HpatError):
    """A test case was aborted (for example, protection tripped)."""
