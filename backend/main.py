import os
import urllib.request
import zipfile
from tqdm import tqdm
import uvicorn
from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

origin = [
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

def install_ffmpeg():
    ffmpeg_path_project = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg-7.1.1-essentials_build", "bin", "ffmpeg.exe")

    if os.path.exists(ffmpeg_path_project):
        print("FFmpeg already installed")
        return ffmpeg_path_project

    print("Installing FFmpeg...")

    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    download_folder = os.path.join(os.getcwd(), "ffmpeg")
    download_path = os.path.join(download_folder, "ffmpeg-release-essentials.zip")

    if not os.path.exists(download_folder):
        print("Creating directory for FFmpeg...")
        os.makedirs(download_folder)

    with tqdm(unit="B", unit_scale=True, miniters=1, desc="Downloading FFmpeg") as pbar:
        urllib.request.urlretrieve(ffmpeg_url, download_path, reporthook=lambda block_num, block_size, total_size: pbar.update(block_num * block_size - pbar.n))

    print("Extracting FFmpeg...")
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(download_folder)

    os.remove(download_path)
    print("FFmpeg zip file removed.")

    if os.path.exists(ffmpeg_path_project):
        print("FFmpeg installed")
        return ffmpeg_path_project
    else:
        print("FFmpeg failed to install")
        return None

if __name__ == "__main__":
    ffmpeg_path = install_ffmpeg()
    uvicorn.run(app, host="0.0.0.0", port=8000)
