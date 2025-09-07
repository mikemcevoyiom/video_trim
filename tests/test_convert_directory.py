from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from video_trim.gui import convert_directory_to_mkv


def test_convert_directory_to_mkv(tmp_path, monkeypatch):
    """Non-MKV videos in a directory tree are converted with ffmpeg copy."""
    # Set up files
    (tmp_path / "video1.mp4").write_text("a")
    subdir = tmp_path / "sub"
    subdir.mkdir()
    (subdir / "video2.mov").write_text("b")
    # Existing MKV should be ignored
    (tmp_path / "skip.mkv").write_text("c")

    commands: list[list[str]] = []

    def fake_run(cmd: list[str], check: bool) -> subprocess.CompletedProcess[str]:
        commands.append(cmd)
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = convert_directory_to_mkv(str(tmp_path))

    expected1 = tmp_path / "converted" / "video1.mkv"
    expected2 = subdir / "converted" / "video2.mkv"
    assert sorted(result) == [str(expected1), str(expected2)]
    assert len(commands) == 2
    assert commands[0][0] == "ffmpeg"
