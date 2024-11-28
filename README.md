# Pytube Tool

<p align="center">
 <img height="150" src="https://raw.githubusercontent.com/h471x/youtube_downloader/master/imgs/pytube.png"/>
</p>

<div align="center">

<p>

``pytube-tool`` is a Python-based command-line utility for downloading YouTube videos. By simply providing a YouTube video URL, users can select their preferred format and download the video efficiently. 

</p>

### Contents

[Features](#features) |
[Installation](#installation) |
[Install from PyPI](#option-1-install-from-pypi) |
[Build from Source](#option-2-build-from-source) |
[Usage](#usage) |
[Example Usage](#example-usage) |
[Development](#development)

</div>

## Features

- **Command-Line Interface (CLI)**: Download YouTube videos using simple terminal commands.
- **Format Selection**: Choose from available video and audio formats before downloading.
- **High-Quality Video**: Supports downloading videos in resolutions such as 720p, 1080p, and higher, if available.
- **Audio-Only Downloads**: Extract and download the audio portion of a video.
- **Batch Downloading**: Download multiple videos using a list of URLs from a file.
- **Fast and Efficient**: Optimized to download videos quickly while maintaining quality.

## Installation

### Option 1: Install from PyPI

To install `pytube-tool` directly from PyPI:

```bash
pip install pytube-tool
```

### Option 2: Build from Source

For those who prefer to build it themselves:

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/h471x/youtube_downloader.git
   cd youtube_downloader
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

4. Install the package:

   ```bash
   pip install dist/*.whl
   ```

## Usage

Once the package is installed, you can use the `pytube` command from the terminal. The script accepts the following command-line arguments:

- **Download Video**:
  - Provide the URL of the YouTube video you wish to download. 

- **Format Selection**:
  - During the download process, the tool will list available formats (video resolutions and audio-only) and prompt you to select one.

- **Batch Processing**:
  - Use a file containing a list of YouTube video URLs to download multiple videos at once.

- **Help Option**:
  - `-h` or `--help`: Display the help message with all available options.

### Example Usage

1. **Download a Single Video**:
   ```bash
   pytube --url https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

   The tool will list available formats, allowing you to select your preferred option.

2. **Batch Download**:
   ```bash
   pytube -b urls.txt
   ```

   `urls.txt` should contain one YouTube URL per line.

3. **Help Option**:
   For help with command-line options, use:
   ```bash
   pytube -h
   ```

## Development

To modify or extend the functionality, ensure you have the required dependencies installed. You can add new features or optimize existing ones as needed.

### Adding New Features

- **Support for Playlists**: Extend the tool to handle full playlist downloads.
- **Download Progress Indicator**: Implement a visual progress bar for downloads.
- **Improved Format Filtering**: Enhance format selection to include additional criteria like frame rate or bit rate.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests with improvements or bug fixes. Your contributions help make the `pytube-tool` better!