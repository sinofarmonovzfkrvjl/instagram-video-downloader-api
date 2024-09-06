from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from instagram import Instagram
from time import sleep

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return """this is instagram video downloader API
    
    Bu instagramdan video yuklovchi API"""

media = None

@app.get("/api/v1/download")
async def download(url):
    try:
        os.remove("video.mp4")
    except:
        pass
    try:
        os.remove("image.png")
    except:
        pass
    
    if url.startswith("https://www.instagram.com/p/"):
        global media
        media = "photo"
        description = Instagram(url).download_photo()
        if description:
            return {"description": description, "url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        elif not description:
            return {"url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        sleep(5)
        os.remove("image.png")
        
    else:
        media = "video"
        description = Instagram(url).download_video()
        if description:
            return {"description": description, "url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        elif not description:
            return {"url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        sleep(5)
        os.remove("video.mp4")
        
@app.get("/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf")
async def get_media():
    if media == "photo":
        def iterimage():
                os.path.join("image.png")
                with open("image.png", "rb") as image:
                    yield from image
        
        return StreamingResponse(iterimage(), media_type="image/png")
    elif media == "video":
        def itervideo():
                os.path.join("video.mp4")
                with open("video.mp4", "rb") as video:
                    yield from video

        return StreamingResponse(itervideo(), media_type="video/mp4")
        
@app.get("/contact-admin")
async def contact_admin():
    return {"message": "https://t.me/sinofarmonov"}
