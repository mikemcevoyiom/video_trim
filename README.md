# video_trim

codex/add-pyproject.toml-for-dependencies
Using ffmpeg to trim video to supplied time frames and reencode to mkv file type and HEVC codec.

## Requirements

- Python 3.8+

## Installation

Install dependencies with [pip](https://pip.pypa.io/):

```bash
python -m pip install --upgrade pip
pip install -e .
```

The command installs the packages listed in `pyproject.toml`, such as `ffmpeg-python` and `click`, and makes `video_trim` available in editable mode.
## Overview
`video_trim` demonstrates how to trim and reencode video segments using FFmpeg. The examples output MKV files encoded with the HEVC (H.265) codec.

## Prerequisites
- FFmpeg 4.x or later with `libx265` support.
- A terminal or command prompt.

Verify FFmpeg installation:

```bash
ffmpeg -version
```

## Installation
Clone the repository:

```bash
git clone https://github.com/your-user-name/video_trim.git
cd video_trim
```

No additional build steps are required.

## Usage examples
### Trim a clip and keep original audio
```bash
ffmpeg -ss 00:00:05 -to 00:00:20 -i input.mp4 -c:v libx265 -c:a copy output.mkv
```
*Output:* `output.mkv` containing the selected time span, video reencoded to HEVC and original audio copied.

### Trim and reencode both audio and video
```bash
ffmpeg -ss 00:02:00 -to 00:03:30 -i input.mp4 -c:v libx265 -c:a aac -b:a 192k clip.mkv
```
*Output:* `clip.mkv` encoded with HEVC video and AAC audio.

## Contribution guidelines
1. Fork the repository and create a new branch.
2. Make your changes with clear commit messages.
3. Run any relevant tests.
4. Submit a pull request describing your changes.

## Roadmap
- Batch processing for multiple clips.
- Support for additional formats and codecs.
- Cross-platform helper scripts.

## Reporting issues and requesting features
Use the GitHub [issue tracker](https://github.com/your-user-name/video_trim/issues) to report bugs or suggest enhancements. Please provide as much detail as possible, including command examples and logs.

main
