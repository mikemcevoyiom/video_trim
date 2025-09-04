import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

from . import __version__


class VideoTrimApp(tk.Tk):
    """Simple GUI to select a video file and display its name."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Video Trim")
        self.geometry("500x300")

        self.file_path: str | None = None

        self.file_label = tk.Label(self, text="No file selected")
        self.file_label.pack(pady=5)

        self.remaining_label = tk.Label(self, text="Time remaining: N/A")
        self.remaining_label.pack(pady=5)

        tk.Button(self, text="Select Video", command=self.select_file).pack(pady=5)

        time_frame = tk.Frame(self)
        time_frame.pack(pady=5, fill="x", padx=10)

        start_frame = tk.Frame(time_frame)
        start_frame.pack(side="left")
        tk.Label(start_frame, text="Start Time (HH:MM:SS)").pack(anchor="w")
        self.start_entry = tk.Entry(start_frame)
        self.start_entry.pack()

        end_frame = tk.Frame(time_frame)
        end_frame.pack(side="right")
        tk.Label(end_frame, text="End Time (HH:MM:SS)").pack(anchor="e")
        self.end_entry = tk.Entry(end_frame)
        self.end_entry.pack()

        tk.Button(self, text="Trim and Convert", command=self.trim_and_convert).pack(pady=10)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        tk.Label(bottom_frame, text=f"Version {__version__}").pack(side="left", padx=10)
        tk.Button(bottom_frame, text="Exit", command=self.quit).pack(side="right", padx=10)

    def select_file(self) -> None:
        """Open a file dialog and display the selected file name."""
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))

    def trim_and_convert(self) -> None:
        """Trim the selected video and convert it to MKV with HEVC codec."""
        if not self.file_path:
            messagebox.showerror("Error", "No video file selected")
            return

        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not start or not end:
            messagebox.showerror("Error", "Start and end times are required")
            return

        output_dir = os.path.join(os.path.dirname(self.file_path), "converted")
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(self.file_path))[0] + ".mkv"
        output_file = os.path.join(output_dir, base_name)

        command = [
            "ffmpeg",
            "-i",
            self.file_path,
            "-ss",
            start,
            "-to",
            end,
            "-c:v",
            "libx265",
            "-c:a",
            "copy",
            output_file,
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as exc:  # pragma: no cover - subprocess failure
            messagebox.showerror("Error", f"FFmpeg failed: {exc}")
            return

        messagebox.showinfo("Success", f"Video saved to {output_file}")


if __name__ == "__main__":  # pragma: no cover - GUI entry point
    app = VideoTrimApp()
    app.mainloop()
