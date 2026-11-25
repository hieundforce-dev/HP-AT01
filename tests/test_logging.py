"""Tests for logging setup (T02)."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from hpat.core.logging_setup import setup_logging


def flush_handlers(logger: logging.Logger) -> None:
    for handler in logger.handlers:
        handler.flush()


def test_file_log_uses_agreed_format(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "run.log"
    logger = setup_logging(log_file, verbose=True)

    logging.getLogger("hpat.demo").info("hello")
    logging.getLogger("hpat.demo").debug("TX VSET1:12.00")
    flush_handlers(logger)

    text = log_file.read_text(encoding="utf-8")
    assert re.search(r"^\d{2}:\d{2}:\d{2}\.\d{3} INFO  hpat\.demo — hello$", text, re.MULTILINE)
    assert re.search(
        r"^\d{2}:\d{2}:\d{2}\.\d{3} DEBUG hpat\.demo — TX VSET1:12\.00$", text, re.MULTILINE
    )


def test_verbose_controls_console_level(tmp_path: Path) -> None:
    quiet = setup_logging(tmp_path / "quiet.log", verbose=False)
    assert quiet.handlers[0].level == logging.INFO

    loud = setup_logging(tmp_path / "loud.log", verbose=True)
    assert loud.handlers[0].level == logging.DEBUG


def test_setup_is_idempotent(tmp_path: Path) -> None:
    setup_logging(tmp_path / "a.log")
    logger = setup_logging(tmp_path / "b.log")
    assert len(logger.handlers) == 2  # one console + one file
