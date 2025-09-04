import os
import tkinter as tk
from tkinter import filedialog

from . import __version__


class VideoTrimApp(tk.Tk):
    """Simple GUI to select a video file and display its name."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Video Trim")
        self.geometry("500x200")

        tk.Label(self, text=f"Version {__version__}").pack(pady=10)

        self.file_label = tk.Label(self, text="No file selected")
        self.file_label.pack(pady=20)

        tk.Button(self, text="Select Video", command=self.select_file).pack()

    def select_file(self) -> None:
        """Open a file dialog and display the selected file name."""
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.*")])
        if file_path:
            self.file_label.config(text=os.path.basename(file_path))


if __name__ == "__main__":  # pragma: no cover - GUI entry point
    app = VideoTrimApp()
    app.mainloop()
