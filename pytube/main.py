import os
import argparse
from pathlib import Path
import subprocess
import sys

# Determine if the script is being run as standalone or as a package
is_standalone = __name__ == "__main__"

# Import based on execution context
if is_standalone:
    from classes.downloader import VideoDownloader
    from classes.formatter import VideoFormatter

    from utils.download_path import prompt_download_path
    from utils.env_handler import get_env_variable, set_env_variable

    __version__ = '0.1.2'
    __author__ = 'Hatix Ntsoa'
else:
    from pytube.classes.downloader import VideoDownloader
    from pytube.classes.formatter import VideoFormatter

    from pytube.utils.download_path import prompt_download_path
    from pytube.utils.env_handler import get_env_variable, set_env_variable

    from pytube import __version__, __author__


def upgrade_package():
    """Upgrade the pytube package using pip."""
    try:
        print("Upgrading pytube to the latest version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pytube"])
        print("Upgrade successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error upgrading pytube: {e}")
        sys.exit(1)

def get_download_path(custom_path=None):
    # Use the custom path if provided
    if custom_path:
        download_path = Path(custom_path).resolve()
        if not download_path.exists():
            print(f"Creating directory: {download_path}")
            download_path.mkdir(parents=True, exist_ok=True)
        set_env_variable("DEFAULT_DOWNLOAD_PATH", str(download_path))
        return download_path

    # Get or set default download path
    download_path = get_env_variable("DEFAULT_DOWNLOAD_PATH")
    if not download_path:
        while True:
            download_path = prompt_download_path()

            if download_path == ".":
                # Handle the case of '.' by converting to absolute path and creating 'pytube_downloads'
                download_path = Path(os.getcwd()) / "pytube_downloads"
                download_path.mkdir(parents=True, exist_ok=True)
                set_env_variable("DEFAULT_DOWNLOAD_PATH", str(download_path))
                break
            elif download_path:
                set_env_variable("DEFAULT_DOWNLOAD_PATH", download_path)
                break  # Exit loop if a valid path is entered
            else:
                print("Invalid path. Please provide a valid download path.")

    return download_path


def process_url(url, download_path):
    """Process a single YouTube URL."""
    try:
        downloader = VideoDownloader(url, download_path)
        downloader.get_preferred_formats()

        if downloader.preferred_formats:
            # Use the formatter to select a format
            format_id_choice = VideoFormatter.select_format(downloader.preferred_formats)
            if format_id_choice:
                downloader.download_and_merge_video(format_id_choice)
            else:
                print("No format selected for URL:", url)
        else:
            print("No preferred formats available for download for URL:", url)
    except Exception as e:
        print(f"Error processing URL {url}: {e}")


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Download YouTube videos using pytube-tool.")
    parser.add_argument(
        "--version", "-v", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--author", 
        action="store_true", 
        help="Show author information"
    )
    parser.add_argument(
        "--url", "-u", 
        type=str, 
        help="YouTube video URL to download directly without prompting."
    )
    parser.add_argument(
        "--path", "-p", 
        type=str, 
        help="Specify the download path for the videos."
    )
    parser.add_argument(
        "--batch", "-b",
        type=str,
        help="Path to a file containing a list of YouTube video URLs."
    )
    parser.add_argument(
        "--upgrade", 
        action="store_true", 
        help="Upgrade the pytube package to the latest version"
    )

    args = parser.parse_args()

    try:
        # Use the provided path or fallback to the default path logic
        download_path = get_download_path(args.path)

        if args.author:
            print(f"pytube-tool is created by {__author__}")
            return 0
        
        if args.upgrade:
            upgrade_package()
            return 0

        if args.batch:
            # Process batch download
            batch_file = Path(args.batch)
            if not batch_file.exists():
                print(f"Batch file not found: {args.batch}")
                return

            with batch_file.open("r") as f:
                urls = [line.strip() for line in f if line.strip()]
            
            if not urls:
                print("No valid URLs found in the batch file.")
                return

            print(f"Starting batch download for {len(urls)} videos.")
            for url in urls:
                print(f"\nProcessing URL: {url}")
                process_url(url, download_path)
        elif args.url:
            # Process single URL download
            process_url(args.url, download_path)
        else:
            # Prompt user for a single URL if not provided
            url = input("Enter the YouTube video URL: ")
            process_url(url, download_path)
    except KeyboardInterrupt:
        print("\nUser canceled.")


if __name__ == '__main__':
    main()