"""Tests for command line interface."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from video_trim.cli import trim_video


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


def test_trim_video_invalid_time(monkeypatch) -> None:
    """Providing an invalid time raises ``ValueError`` before running FFmpeg."""

    def fake_run(cmd: list[str], check: bool) -> subprocess.CompletedProcess[str]:  # pragma: no cover - not executed
        raise AssertionError("FFmpeg should not be invoked")

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(ValueError):
        trim_video("in.mp4", "00:00", "00:00:10", "out.mp4")


def test_cli_invalid_time() -> None:
    """The CLI reports an error for an invalid time format."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "video_trim",
            "input.mp4",
            "00:00:00",
            "invalid",
            "output.mp4",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "Invalid end time" in result.stderr
