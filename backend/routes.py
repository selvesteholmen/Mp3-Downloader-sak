from fastapi import APIRouter
from pydantic import BaseModel
from Downloading import spotify_download, youtube_download

router = APIRouter()

class SpotifyRequest(BaseModel):
    search: str

class YoutubeRequest(BaseModel):
    link: str

@router.post("/spotify_download")
def download_spotify_song(request: SpotifyRequest):
    spotify_download(request.search)
    return {"message": f"Downloading: {request.search}"}

@router.post("/youtube_download")
def download_youtube_video(request: YoutubeRequest):
    youtube_download(request.link)
    return {"message": f"Downloading: {request.link}"}