import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from utils.ffmpeg_helper import get_ffmpeg_path

origin = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    ffmpeg_path = get_ffmpeg_path()
    uvicorn.run(app, host="0.0.0.0", port=8000)
