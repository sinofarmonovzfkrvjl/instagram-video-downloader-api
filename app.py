from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from instagram import Instagram

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return """this is instagram video downloader API
    
    Bu instagramdan video yuklovchi API"""

@app.get("/api/v1/download")
async def download(url):
    try:
        os.remove("video.mp4")
        os.remove("image.png")
    except:
        pass
    if url.startswith("https://www.instagram.com/reel/") and url.endswith("https://www.instagram.com/stories/"):
        if Instagram(url).download_video():
            def itervideo():
                # os.path.join("video.mp4")
                with open("video.mp4", "rb") as video:
                    yield from video

            return StreamingResponse(itervideo(), media_type="video/mp4")
        else:
            return "ERROR"
            
    elif url.startswith("https://www.instagram.com/p/"):
        if Instagram(url).download_photo():
            def iterimage():
                # os.path.join("image.png")
                with open("image.png", "rb") as image:
                    yield from image

            return StreamingResponse(iterimage(), media_type="image/png")

        else:
            return "ERROR"
    else:
        return "This is not instagram video's url"
