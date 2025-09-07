"""Core package for video trimming.

This package currently provides a command line interface and placeholder
functionality for trimming videos with FFmpeg. Additional features will
be implemented in future iterations.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("video_trim")
except PackageNotFoundError:  # pragma: no cover - fallback when not installed
    __version__ = "0.0.0"

__all__ = ["__version__"]
