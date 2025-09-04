"""Command line interface for video_trim."""

import argparse


__version__ = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trim video using ffmpeg.")
    parser.add_argument("input", nargs="?", help="Input video file")
    parser.add_argument("output", nargs="?", help="Output video file")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
