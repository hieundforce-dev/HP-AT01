"""Run folder creation.

Layout (see ``docs/DESIGN.md``)::

    runs/2026-11-25_143012_<plan>_<dut-sn>/
    ├── plan_copy.csv
    ├── results/
    ├── waveforms/
    └── logs/run.log
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hpat.core.errors import PlanError

TIMESTAMP_FORMAT = "%Y-%m-%d_%H%M%S"
MAX_SLUG_LENGTH = 40

_UNSAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True)
class RunFolder:
    """Paths of one test run."""

    root: Path
    results: Path
    waveforms: Path
    logs: Path
    log_file: Path
    plan_copy: Path


def slugify(value: str, default: str = "NA") -> str:
    """Turn arbitrary text into a safe folder-name component."""
    cleaned = _UNSAFE_CHARS.sub("_", value.strip())
    cleaned = cleaned.strip("._-")
    return cleaned[:MAX_SLUG_LENGTH] or default


def build_run_name(plan_path: Path | str, dut_sn: str, timestamp: datetime | None = None) -> str:
    """Build ``<timestamp>_<plan-stem>_<dut-sn>``."""
    stamp = (timestamp or datetime.now()).strftime(TIMESTAMP_FORMAT)
    plan_slug = slugify(Path(plan_path).stem, default="plan")
    sn_slug = slugify(dut_sn, default="NA")
    return f"{stamp}_{plan_slug}_{sn_slug}"


def create_run_folder(
    runs_root: Path | str,
    plan_path: Path | str,
    dut_sn: str = "NA",
    timestamp: datetime | None = None,
    copy_plan: bool = True,
) -> RunFolder:
    """Create the run folder tree and return its paths.

    An existing folder is never reused: ``_2``, ``_3``, ... is appended when the
    same plan runs twice within one second.

    Raises:
        PlanError: ``copy_plan`` is true and the plan file does not exist.
    """
    plan = Path(plan_path)
    if copy_plan and not plan.is_file():
        raise PlanError(f"Plan file not found: {plan}")

    root_base = Path(runs_root) / build_run_name(plan, dut_sn, timestamp)
    root = root_base
    counter = 2
    while root.exists():
        root = root_base.with_name(f"{root_base.name}_{counter}")
        counter += 1

    results = root / "results"
    waveforms = root / "waveforms"
    logs = root / "logs"
    for directory in (results, waveforms, logs):
        directory.mkdir(parents=True, exist_ok=False)

    plan_copy = root / "plan_copy.csv"
    if copy_plan:
        shutil.copy2(plan, plan_copy)

    return RunFolder(
        root=root,
        results=results,
        waveforms=waveforms,
        logs=logs,
        log_file=logs / "run.log",
        plan_copy=plan_copy,
    )
