import yt_dlp
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import re
import threading
import itertools
import sys
import time


class VideoDownloader:
    def __init__(self, url, download_path=None) -> None:
        self.url: str = url
        self.video_title = None
        self.preferred_formats = {}
        self.audio_formats = []
        self.download_path = download_path or os.getcwd()

        # Ensure the download directory exists
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize the filename by removing or replacing characters that are not allowed in filenames."""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def get_preferred_formats(self):
        """Retrieve preferred formats (1080p, 720p, 480p, 360p) and indicate audio presence."""
        preferred_qualities = ["1080p", "720p", "480p", "360p"]

        stop_flag = threading.Event()
        animation_thread = threading.Thread(target=self._loading_animation, args=(stop_flag,))
        animation_thread.start()

        def progress_hook(d):
            """Custom progress hook to stop animation when download progress begins."""
            if d['status'] == 'downloading':
                stop_flag.set()  # Stop animation when download starts
            elif d['status'] == 'extracting':
                sys.stdout.write("\rProcessing download... Extracting video data")
                sys.stdout.flush()

        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'progress_hooks': [progress_hook]}) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                if not info_dict:
                    print("\nFailed to retrieve video information.")
                    return None

                formats = info_dict.get('formats', [])
                if not formats:
                    print("\nNo formats found for this video.")
                    return None

                # Store the video title and sanitize it for file names
                self.video_title = self.sanitize_filename(info_dict.get('title', 'video'))

                # Filter only preferred formats
                for f in formats:
                    quality = f.get('format_note')
                    if quality in preferred_qualities:
                        has_audio = f.get('acodec') != 'none'
                        self.preferred_formats[f.get('format_id')] = {
                            'id': f.get('format_id'),
                            'has_audio': has_audio,
                            'filesize': f.get('filesize') or "Unknown",
                            'format_note': quality,
                        }
                    elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':  # Audio-only format
                        self.audio_formats.append(f.get('format_id'))

        except Exception as e:
            print(f"\nAn error occurred while retrieving formats: {e}")
        finally:
            # Ensure the animation stops if it hasn't already
            stop_flag.set()
            animation_thread.join()

    def _loading_animation(self, stop_flag):
        """Display a loading animation."""
        for char in itertools.cycle(['|', '/', '-', '\\']):
            if stop_flag.is_set():
                break
            sys.stdout.write(f"\rProcessing download... {char}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\rProcessing download... Done!\n")
        sys.stdout.flush()

    def _run_with_loading(self, func, *args, **kwargs):
        """Run a function with a loading animation."""
        stop_flag = threading.Event()
        thread = threading.Thread(target=self._loading_animation, args=(stop_flag,))
        thread.start()

        try:
            func(*args, **kwargs)
        finally:
            stop_flag.set()
            thread.join()

    def download_and_merge_video(self, format_id_choice):
        """Download chosen video format with audio (merging audio if necessary)."""
        chosen_format = self.preferred_formats.get(format_id_choice)
        if not chosen_format:
            print(f"Selected format ID '{format_id_choice}' is not available.")
            return

        video_output = os.path.join(self.download_path, f"{self.video_title}.mp4")

        if chosen_format['has_audio']:
            # Download directly if audio is included
            ydl_opts = {
                'format': chosen_format['id'],
                'outtmpl': video_output,
                'noplaylist': True,
                'quiet': True,
                'ignoreerrors': True,
                'no_warnings': True,
            }
            self._run_with_loading(self._download_video, ydl_opts)
        else:
            # Download video without audio and merge with audio if available
            video_temp = os.path.join(self.download_path, f"{self.video_title}_video.mp4")
            audio_temp = os.path.join(self.download_path, f"{self.video_title}_audio.mp4")

            ydl_opts_video = {
                'format': chosen_format['id'],
                'outtmpl': video_temp,
                'noplaylist': True,
                'quiet': True,
                'ignoreerrors': True,
                'no_warnings': True,
            }
            ydl_opts_audio = {
                'format': self.audio_formats[0],
                'outtmpl': audio_temp,
                'noplaylist': True,
                'quiet': True,
                'ignoreerrors': True,
                'no_warnings': True,
            }

            # self._run_with_loading(self._download_video, ydl_opts_video)
            # self._run_with_loading(self._download_video, ydl_opts_audio)

            self._download_video(ydl_opts_video)
            self._download_video(ydl_opts_audio)

            # Merge video and audio using MoviePy
            # self._run_with_loading(self._merge_video_audio, video_temp, audio_temp, video_output)
            self._merge_video_audio(video_temp, audio_temp, video_output)

    def _download_video(self, ydl_opts):
        """Download video or audio with yt_dlp."""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def _merge_video_audio(self, video_temp, audio_temp, output_file):
        """Merge video and audio into one file."""
        try:
            video_clip = VideoFileClip(video_temp)
            audio_clip = AudioFileClip(audio_temp)

            # Set the audio of the video clip
            video_clip = video_clip.set_audio(audio_clip)

            # Write the result to the specified directory
            video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

            # Clean up temporary files
            video_clip.close()
            audio_clip.close()
            os.remove(video_temp)
            os.remove(audio_temp)
            print(f"Merged video saved as: {output_file}")
            print("Temporary video and audio files deleted.")

        except Exception as e:
            print(f"An error occurred while merging video and audio: {e}")
