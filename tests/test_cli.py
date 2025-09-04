"""Tests for command line interface."""

from __future__ import annotations

import subprocess
import sys


def test_cli_help() -> None:
    """Running the CLI with ``--help`` should succeed."""
    result = subprocess.run(
        [sys.executable, "-m", "video_trim", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
