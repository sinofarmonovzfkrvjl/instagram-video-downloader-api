from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware import cors
import os
from instagram import Instagram
from time import sleep
import aiohttp
from bs4 import BeautifulSoup
from yarl import URL

app = FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/", include_in_schema=False)
async def root():
    return """this is instagram video downloader API
    
    Bu instagramdan video yuklovchi API"""

media = None

@app.get("/api/v1/download")
async def download(url: str):
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

class Instagram:
    @staticmethod
    async def _fetch(session, url):
        async with session.get(url) as response:
            return await response.read()

    @staticmethod
    async def get_info(url: str):
        main_url = URL("https://ddinstagram.com")

        async with aiohttp.ClientSession() as session:
            async with session.get(url.replace("www.", "dd")) as response:
                resp = await response.read()

            soup = BeautifulSoup(resp.decode("utf-8"), "html.parser")
            profile = soup.find("meta", {"name": "twitter:title"}).get("content")
            description = soup.find("meta", property="og:description").get("content")
            download_urls = []

            video_path = soup.find("meta", property="og:video")
            image_path = soup.find("meta", property="og:image")

            if video_path:
                type_ = "Video"
                get_url = main_url.with_path(video_path["content"])

                async with session.get(get_url) as response_:
                    resp = response_.url

                    if not resp == get_url:
                        download_urls.append(str(resp))

            else:
                path_ = image_path["content"]
                post_id = path_.split("/")[2]

                if "grid" in path_:
                    type_ = "Album"
                    paths = (f"/images/{post_id}/{i}" for i in range(1, 11))

                    for path_ in paths:
                        get_url = main_url.with_path(path_)
                        async with session.get(get_url) as response_:
                            resp = response_.url

                            if resp == get_url:
                                break
                            download_urls.append(str(resp))

                else:
                    type_ = "Image"

                    get_url = main_url.with_path(path_)
                    async with session.get(get_url) as response_:
                        resp = response_.url
                        if not get_url == resp:
                            download_urls.append(str(resp))

            response = {
                "Profile": profile,
                "Caption": description,
                "type": type_,
                "url": download_urls if len(download_urls) > 1 else download_urls[0],
            }
            return response

@app.post("/instagram/")
async def get_instagram_media(instagram_url: str):
    try:
        info = await Instagram.get_info(instagram_url)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("myapp:app", host="127.0.0.1", port=8000, reload=True)
