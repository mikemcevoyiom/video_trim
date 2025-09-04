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

        tk.Label(self, text=f"Version {__version__}").pack(pady=10)

        self.file_path: str | None = None

        self.file_label = tk.Label(self, text="No file selected")
        self.file_label.pack(pady=5)

        tk.Button(self, text="Select Video", command=self.select_file).pack(pady=5)

        tk.Label(self, text="Start Time (HH:MM:SS)").pack()
        self.start_entry = tk.Entry(self)
        self.start_entry.pack(pady=5)

        tk.Label(self, text="End Time (HH:MM:SS)").pack()
        self.end_entry = tk.Entry(self)
        self.end_entry.pack(pady=5)

        tk.Button(self, text="Trim and Convert", command=self.trim_and_convert).pack(pady=10)

        tk.Button(self, text="Exit", command=self.quit).pack(side="bottom", anchor="e", padx=10, pady=10)

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
