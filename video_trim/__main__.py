"""Module entry point for ``python -m video_trim``."""

from .cli import main


if __name__ == "__main__":  # pragma: no cover - module entry point
    raise SystemExit(main())
