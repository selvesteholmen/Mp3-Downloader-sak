import yt_dlp
import os
from datetime import datetime
import subprocess
from utils.ffmpeg_helper import get_ffmpeg_path


def download_youtube_audio(url):
    downloads_folder = os.environ.get("DOWNLOADS_PATH", os.path.join(os.path.expanduser("~"), "Downloads"))

    ydl_opts = {
        'format': 'bestaudio/best',
        'noprogress': True,
        'quiet': True,
        'postprocessors': [],
        'nocheckcertificate': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'output').replace(" ", "_")
        output_path = os.path.join(downloads_folder, f"{video_title}.%(ext)s")

        ydl_opts['outtmpl'] = output_path

        ydl = yt_dlp.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info_dict)

    current_time = datetime.now().timestamp()
    os.utime(downloaded_file, (current_time, current_time))

    if downloaded_file.endswith('.webm'):
        mp3_file = downloaded_file.replace('.webm', '.mp3')
        convert_to_mp3(downloaded_file, mp3_file)
        os.remove(downloaded_file)
        print(f"Downloaded and converted audio: {mp3_file}")
    else:
        print(f"Downloaded audio: {downloaded_file}")


def convert_to_mp3(input_file, output_file):
    ffmpeg_path = get_ffmpeg_path()

    with open(os.devnull, 'w') as devnull:
        command = [
            ffmpeg_path,
            '-y',
            '-i', input_file,
            '-vn',
            '-ar', '44100',
            '-ac', '2',
            '-b:a', '192k',
            output_file
        ]
        subprocess.run(command, stdout=devnull, stderr=devnull, check=True)
