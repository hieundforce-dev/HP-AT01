"""Tests for run folder creation (T02)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from hpat.core.errors import PlanError
from hpat.core.runfolder import build_run_name, create_run_folder, slugify

FIXED_TIME = datetime(2026, 11, 25, 14, 30, 12)


def make_plan(tmp_path: Path, name: str = "efficiency buck1.csv") -> Path:
    plan = tmp_path / name
    plan.write_text("test_id\n", encoding="utf-8")
    return plan


def test_build_run_name() -> None:
    assert build_run_name("efficiency buck1.csv", "SN 123/45", FIXED_TIME) == (
        "2026-11-25_143012_efficiency_buck1_SN_123_45"
    )


def test_slugify_handles_empty_and_unsafe_text() -> None:
    assert slugify("  ") == "NA"
    assert slugify("a b/c:d") == "a_b_c_d"
    assert slugify("../etc/passwd") == "etc_passwd"


def test_create_run_folder_layout(tmp_path: Path) -> None:
    plan = make_plan(tmp_path)
    run = create_run_folder(tmp_path / "runs", plan, "SN123", FIXED_TIME)

    assert run.root.name == "2026-11-25_143012_efficiency_buck1_SN123"
    assert run.root.parent == tmp_path / "runs"
    assert run.results.is_dir()
    assert run.waveforms.is_dir()
    assert run.logs.is_dir()
    assert run.log_file == run.logs / "run.log"
    assert run.plan_copy.read_text(encoding="utf-8") == plan.read_text(encoding="utf-8")


def test_same_second_gets_unique_suffix(tmp_path: Path) -> None:
    plan = make_plan(tmp_path)
    first = create_run_folder(tmp_path / "runs", plan, "SN123", FIXED_TIME)
    second = create_run_folder(tmp_path / "runs", plan, "SN123", FIXED_TIME)
    third = create_run_folder(tmp_path / "runs", plan, "SN123", FIXED_TIME)

    assert first.root.name.endswith("_SN123")
    assert second.root.name.endswith("_SN123_2")
    assert third.root.name.endswith("_SN123_3")


def test_empty_dut_sn_becomes_na(tmp_path: Path) -> None:
    run = create_run_folder(tmp_path / "runs", make_plan(tmp_path), "", FIXED_TIME)
    assert run.root.name.endswith("_NA")


def test_missing_plan_raises(tmp_path: Path) -> None:
    with pytest.raises(PlanError, match="Plan file not found"):
        create_run_folder(tmp_path / "runs", tmp_path / "missing.csv", "SN1", FIXED_TIME)
