"""GUI and utility functions for the video_trim project."""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from video_trim import __version__
from video_trim.cli import _validate_time


VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".flv",
    ".wmv",
    ".m4v",
    ".mpg",
    ".mpeg",
}

FILETYPES = (
    "Video files",
    " ".join(f"*{ext}" for ext in sorted(VIDEO_EXTENSIONS)),
)


class VideoTrimApp(tk.Tk):
    """Simple GUI to select a video file and display its name."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Video Trim")
        self.geometry("500x400")

        self.file_path: str | None = None
        self.file_label = tk.Label(self, text="No file selected")
        self.file_label.pack(pady=5)

        self.remaining_label = tk.Label(self, text="Time remaining: N/A")
        self.remaining_label.pack(pady=5)

        tk.Button(
            self, text="Select Video", command=self.select_file
        ).pack(pady=5)
        tk.Button(
            self, text="Trim and Convert", command=self.trim_and_convert
        ).pack(pady=5)

        time_frame = tk.Frame(self)
        time_frame.pack(pady=5, fill="x", padx=10)

        start_frame = tk.Frame(time_frame)
        start_frame.pack(side="left")
        tk.Label(start_frame, text="Start Time (HH:MM:SS)").pack(anchor="w")
        self.time_validator = self.register(self._validate_time_entry)
        self.start_entry = tk.Entry(
            start_frame,
            validate="key",
            validatecommand=(self.time_validator, "%P"),
        )
        self.start_entry.pack()

        end_frame = tk.Frame(time_frame)
        end_frame.pack(side="right")
        tk.Label(end_frame, text="End Time (HH:MM:SS)").pack(anchor="e")
        self.end_entry = tk.Entry(
            end_frame,
            validate="key",
            validatecommand=(self.time_validator, "%P"),
        )
        self.end_entry.pack()

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        tk.Button(
            bottom_frame, text="Exit", command=self.confirm_exit
        ).pack(side="left", padx=10)
        tk.Label(bottom_frame, text=f"Version {__version__}").pack(
            side="right", padx=10
        )

    def select_file(self) -> None:
        """Open a file dialog and display the selected file name."""
        file_path = filedialog.askopenfilename(filetypes=[FILETYPES])
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))

    @staticmethod
    def _validate_time_entry(proposed: str) -> bool:
        """Validate time entry input with a HH:MM:SS mask."""
        if proposed == "":
            return True
        if len(proposed) > 8:
            return False
        for index, char in enumerate(proposed):
            if index in (2, 5):
                if char != ":":
                    return False
            elif not char.isdigit():
                return False
        return True

    def trim_and_convert(self) -> None:
        """Trim the selected video."""
        if not self.file_path:
            messagebox.showerror("Error", "No video file selected")
            return

        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not start or not end:
            messagebox.showerror("Error", "Start and end times are required")
            return

        output_dir = os.path.join(os.path.dirname(self.file_path), "edited")
        os.makedirs(output_dir, exist_ok=True)

        base_name = (
            os.path.splitext(os.path.basename(self.file_path))[0] + ".mkv"
        )
        output_file = os.path.join(output_dir, base_name)

        try:
            _validate_time(start, "start")
            _validate_time(end, "end")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        command = [
            "ffmpeg",
            "-i",
            self.file_path,
            "-ss",
            start,
            "-to",
            end,
            "-c",
            "copy",
            output_file,
        ]

        try:
            subprocess.run(command, check=True)
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "ffmpeg not found. Please install ffmpeg "
                "and ensure it is in your PATH.",
            )
            return
        except subprocess.CalledProcessError as exc:
            # pragma: no cover - subprocess failure
            messagebox.showerror(
                "Error", f"FFmpeg failed: {exc}"
            )
            return

        messagebox.showinfo("Success", f"Video saved to {output_file}")

    def confirm_exit(self) -> None:
        """Prompt the user to confirm application exit."""
        if messagebox.askokcancel("Exit", "Close the application?"):
            # ``destroy`` closes the window and ``quit`` ensures the main loop
            # terminates, allowing the application to exit cleanly.
            self.destroy()
            self.quit()


if __name__ == "__main__":  # pragma: no cover - GUI entry point
    app = VideoTrimApp()
    app.mainloop()
