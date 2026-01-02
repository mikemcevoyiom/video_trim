import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Optional, Set, Tuple

ENCODER_PREFERENCE = [
    "h264_amf",
    "hevc_amf",
    "h264_nvenc",
    "hevc_nvenc",
    "h264_qsv",
    "hevc_qsv",
    "h264_videotoolbox",
    "hevc_videotoolbox",
]

def detect_available_encoders() -> Set[str]:
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return set()

    encoders = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].startswith("V"):
            encoders.add(parts[1])
    return encoders


def select_encoder() -> str:
    encoders = detect_available_encoders()
    for candidate in ENCODER_PREFERENCE:
        if candidate not in encoders:
            continue
        return candidate
    return "libx264"


def ensure_unique_output_path(output_dir: Path, base_name: str, suffix: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate = output_dir / f"{base_name}{suffix}"
    counter = 1
    while candidate.exists():
        candidate = output_dir / f"{base_name}_{counter}{suffix}"
        counter += 1
    return candidate


def build_ffmpeg_command(
    input_path: Path,
    output_path: Path,
    start: str,
    end: str,
    encoder: str,
    bitrate_mbps: Optional[float],
) -> List[str]:
    command = [
        "ffmpeg",
        "-hide_banner",
    ]

    command.extend(
        [
            "-ss",
            start,
            "-to",
            end,
            "-i",
            str(input_path),
            "-c:v",
            encoder,
        ]
    )
    if bitrate_mbps is not None:
        command.extend(["-b:v", f"{bitrate_mbps}M"])
    command.extend(
        [
            "-c:a",
            "copy",
            "-y",
            str(output_path),
        ]
    )
    return command


def run_ffmpeg_with_fallback(
    input_path: Path,
    output_path: Path,
    start: str,
    end: str,
    bitrate_mbps: Optional[float],
) -> Tuple[subprocess.CompletedProcess, str, bool]:
    encoder = select_encoder()
    command = build_ffmpeg_command(
        input_path, output_path, start, end, encoder, bitrate_mbps
    )
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode == 0 or encoder == "libx264":
        return result, encoder, False

    fallback_command = build_ffmpeg_command(
        input_path, output_path, start, end, "libx264", bitrate_mbps
    )
    fallback_result = subprocess.run(
        fallback_command, check=False, capture_output=True, text=True
    )
    return fallback_result, "libx264", True


class VideoTrimGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Video Trim")
        self.geometry("520x240")
        self.resizable(False, False)
        self.selected_file: Optional[Path] = None

        self._build_widgets()

    def _build_widgets(self) -> None:
        file_frame = tk.Frame(self)
        file_frame.pack(fill="x", padx=16, pady=10)

        tk.Label(file_frame, text="Selected file:").pack(anchor="w")
        self.file_label = tk.Label(file_frame, text="No file selected", anchor="w")
        self.file_label.pack(fill="x", pady=(4, 6))

        tk.Button(file_frame, text="Select Video", command=self.select_file).pack(anchor="w")

        time_frame = tk.Frame(self)
        time_frame.pack(fill="x", padx=16, pady=10)

        tk.Label(time_frame, text="Start time (e.g. 00:00:05)").grid(row=0, column=0, sticky="w")
        tk.Label(time_frame, text="End time (e.g. 00:00:20)").grid(row=0, column=1, sticky="w")

        self.start_entry = tk.Entry(time_frame, width=20)
        self.end_entry = tk.Entry(time_frame, width=20)
        self.start_entry.grid(row=1, column=0, padx=(0, 10), pady=(4, 0), sticky="w")
        self.end_entry.grid(row=1, column=1, pady=(4, 0), sticky="w")

        bitrate_frame = tk.Frame(self)
        bitrate_frame.pack(fill="x", padx=16, pady=(0, 10))

        tk.Label(bitrate_frame, text="Target video bitrate (Mbps)").grid(
            row=0, column=0, sticky="w"
        )
        self.bitrate_entry = tk.Entry(bitrate_frame, width=20)
        self.bitrate_entry.insert(0, "8")
        self.bitrate_entry.grid(row=1, column=0, pady=(4, 0), sticky="w")

        action_frame = tk.Frame(self)
        action_frame.pack(fill="x", padx=16, pady=(10, 0))

        self.run_button = tk.Button(action_frame, text="Trim Video", command=self.trim_video)
        self.run_button.pack(anchor="w")

        self.status_label = tk.Label(self, text="", anchor="w", fg="#0a6e0a")
        self.status_label.pack(fill="x", padx=16, pady=(10, 0))

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[
                ("Video files", "*.mp4 *.mkv *.mov *.avi *.webm *.m4v"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            self.selected_file = Path(file_path)
            self.file_label.config(text=str(self.selected_file))
            self.status_label.config(text="")

    def trim_video(self) -> None:
        if not self.selected_file:
            messagebox.showwarning("Missing file", "Please select a video file to trim.")
            return

        start_time = self.start_entry.get().strip()
        end_time = self.end_entry.get().strip()
        bitrate_value = self.bitrate_entry.get().strip()

        if not start_time or not end_time:
            messagebox.showwarning("Missing time", "Please enter both start and end times.")
            return

        bitrate_mbps: Optional[float] = None
        if bitrate_value:
            try:
                bitrate_mbps = float(bitrate_value)
                if bitrate_mbps <= 0:
                    raise ValueError("Bitrate must be positive.")
            except ValueError:
                messagebox.showwarning(
                    "Invalid bitrate",
                    "Please enter a positive number for the bitrate (in Mbps), or leave it blank.",
                )
                return

        output_dir = self.selected_file.parent / "Edited"
        output_path = ensure_unique_output_path(
            output_dir,
            f"{self.selected_file.stem}_trim",
            self.selected_file.suffix,
        )

        self.run_button.config(state="disabled")
        self.status_label.config(text="Running ffmpeg...", fg="#5a5a5a")
        self.update_idletasks()

        try:
            result, encoder, used_fallback = run_ffmpeg_with_fallback(
                self.selected_file,
                output_path,
                start_time,
                end_time,
                bitrate_mbps,
            )
        except FileNotFoundError:
            self.run_button.config(state="normal")
            messagebox.showerror("FFmpeg not found", "FFmpeg was not found on this system.")
            return

        self.run_button.config(state="normal")

        if result.returncode == 0:
            fallback_note = " (fallback to software encoding)" if used_fallback else ""
            self.status_label.config(
                text=f"Saved trimmed video to {output_path}{fallback_note}",
                fg="#0a6e0a",
            )
        else:
            messagebox.showerror(
                "FFmpeg error",
                (
                    f"FFmpeg failed with exit code {result.returncode}.\n"
                    f"Encoder: {encoder}\n\n{result.stderr}"
                ),
            )
            self.status_label.config(text="", fg="#0a6e0a")


def main() -> None:
    app = VideoTrimGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
