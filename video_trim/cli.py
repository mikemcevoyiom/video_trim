"""Command line interface for video trimming using FFmpeg.

This module provides a simple command line interface and placeholder
functionality for trimming videos with FFmpeg. The actual trimming logic
will be expanded in future iterations.
"""

from __future__ import annotations

import argparse
import subprocess
from typing import Sequence

from video_trim import __version__


def trim_video(input_file: str, start: str, end: str, output_file: str) -> None:
    """Trim a video using FFmpeg.

    Parameters
    ----------
    input_file:
        Path to the input video.
    start:
        Start time in ``HH:MM:SS`` format.
    end:
        End time in ``HH:MM:SS`` format.
    output_file:
        Path to the trimmed output video.

    This is a placeholder implementation that invokes FFmpeg. Additional
    validation and error handling will be added later.
    """

    command = [
        "ffmpeg",
        "-i",
        input_file,
        "-ss",
        start,
        "-to",
        end,
        "-c",
        "copy",
        output_file,
    ]

    subprocess.run(command, check=True)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI."""
    parser = argparse.ArgumentParser(description="Trim a video using FFmpeg")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("start", help="Start time (e.g. 00:00:00)")
    parser.add_argument("end", help="End time (e.g. 00:00:10)")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Entry point for the command line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)
    trim_video(args.input, args.start, args.end, args.output)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
