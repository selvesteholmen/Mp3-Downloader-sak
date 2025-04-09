import os
import platform
import urllib.request
import zipfile
from tqdm import tqdm


def get_ffmpeg_path():
    if platform.system() != "Windows":
        return "ffmpeg"

    ffmpeg_path = os.path.join(
        os.getcwd(), "ffmpeg", "ffmpeg-7.1.1-essentials_build", "bin", "ffmpeg.exe"
    )

    if os.path.exists(ffmpeg_path):
        return ffmpeg_path

    print("Installing FFmpeg for Windows...")

    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    download_folder = os.path.join(os.getcwd(), "ffmpeg")
    download_path = os.path.join(download_folder, "ffmpeg-release-essentials.zip")

    os.makedirs(download_folder, exist_ok=True)

    with tqdm(unit="B", unit_scale=True, miniters=1, desc="Downloading FFmpeg") as pbar:
        urllib.request.urlretrieve(
            ffmpeg_url,
            download_path,
            reporthook=lambda block_num, block_size, total_size: pbar.update(
                block_num * block_size - pbar.n
            ),
        )

    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall(download_folder)

    os.remove(download_path)

    return ffmpeg_path if os.path.exists(ffmpeg_path) else None
