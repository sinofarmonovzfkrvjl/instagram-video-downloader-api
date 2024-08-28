from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from instagram import Instagram
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return "this is instagram video downloader API\n\nBu instagramdan video yuklovchi API"

@app.get("/api/v1/download")
async def download(url):
    try:
        os.remove("video.mp4")
    except:
        pass
    if url.startswith("https://www.instagram.com/reel/"):
        Instagram(url).download_video()
    elif url.startswith("https://www.instagram.com/p/"):
        Instagram(url).download_photo()
    
    def iterfile():
        os.path.join("video.mp4")
        with open("video.mp4", "rb") as file_like:
            yield from file_like
    
    return StreamingResponse(iterfile(), media_type="video/mp4")
