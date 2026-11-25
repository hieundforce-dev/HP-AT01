"""Logging setup.

Console output is handled by Rich; the run log file uses the format agreed in
``docs/DESIGN.md``: ``HH:MM:SS.mmm LEVEL module — message``.
"""

from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler

FILE_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)-5s %(name)s — %(message)s"
FILE_DATE_FORMAT = "%H:%M:%S"

ROOT_LOGGER_NAME = "hpat"


def setup_logging(log_file: Path | str | None = None, verbose: bool = False) -> logging.Logger:
    """Configure the ``hpat`` logger.

    Args:
        log_file: When given, DEBUG records are also written to this file.
        verbose: Show DEBUG records on the console (including raw SCPI TX/RX).

    Returns:
        The configured ``hpat`` logger.
    """
    logger = logging.getLogger(ROOT_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    console = RichHandler(
        rich_tracebacks=True,
        show_path=False,
        markup=False,
        show_time=True,
        log_time_format=FILE_DATE_FORMAT,
    )
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

    if log_file is not None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8", delay=True)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(FILE_FORMAT, datefmt=FILE_DATE_FORMAT))
        logger.addHandler(file_handler)

    return logger
