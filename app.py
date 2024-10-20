from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware import cors
import os
from instagram import InstagramV1
from time import sleep
import aiohttp
from bs4 import BeautifulSoup
from yarl import URL

app = FastAPI(
    docs_url='/',
    title="Instagram Media Downloder API | t.me/sinofarmonov2",
    description="This is Instagram Media Downloader API",
    version="1.0.0",
    summary="contact admin: https://t.me/sinofarmonov2",
)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

media = None

@app.get("/api/v1/download", tags=['Version 1'], name="Instagram Media Downloader API Free")
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
        description = InstagramV1(url).download_photo()
        if description:
            return {"description": description, "url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        elif not description:
            return {"url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        sleep(5)
        os.remove("image.png")
        
    else:
        media = "video"
        description = InstagramV1(url).download_video()
        if description:
            return {"description": description, "url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        elif not description:
            return {"url": "/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf"}
        sleep(5)
        os.remove("video.mp4")
        
@app.get("/api/v1/get-videoihfnejndgiuf/iuh43rwehbndsijrewbbfdhbfdjhfjdsfhjdsf", tags=['Version 1'], include_in_schema=False    )
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

@app.get("/api/v2/download", tags=['Version 2'], name="Instagram Media Downloader API Paid")
async def get_instagram_media(url: str, token: str):
    if token == open('token.txt', 'r').read():
        try:
            info = await Instagram.get_info(url)
            return info
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Token is incorrect")