"""Utility helpers for mendeley-watchdog"""

import logging
import os

from typing import Sequence


def append_file_ext(*files, ext: str = None, f_ext: Sequence = None) -> list:
    """Appends either one or multiple extensions to list of strings"""

    if ext is not None and f_ext is not None:
        raise ValueError("specify either 'ext or 'f_ext'" + " not both")
    if f_ext is not None and len(f_ext) != len(files):
        raise ValueError("'f_ext' must have many items as number of files")

    if f_ext is not None:
        files_ext = [
            f"{filename}.{f_ext[filecount]}"
            if not filename.endswith(f_ext[filecount]) else filename
            for filecount, filename in enumerate(files)
        ]
    elif ext is not None:
        files_ext = [
            f"{filename}.{ext}"
            if not filename.endswith(ext) else filename
            for filename in files
        ]
    else:
        raise ValueError("neither 'ext or 'f_ext' are specified")
    return files_ext


def isdir(path: str) -> str:
    """Empty if expanded user or abstract paths point to a directory"""

    if not path:
        return ""
    if path.startswith("~"):
        path = os.path.expanduser(path)
    elif path.startswith("."):
        path = os.path.abspath(path)
    normed_path = os.path.normpath(path)
    if os.path.isdir(normed_path):
        return normed_path
    return ""


def setup_logging(filename) -> str:
    """Log info to stderr and debug to file in workdir"""

    log_format = "%(asctime)s - %(name)20s - %(levelname)-10s %(message)s"
    logging.basicConfig(
        filename=filename,
        level=10,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=log_format
    )

    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(console_logger)
