import requests
from bs4 import BeautifulSoup

class Instagram:
    def __init__(self, url: str):
        self.url = url
    
    def download_video(self):
        url = self.url.replace("www.", "d.dd")
        res = requests.get(url)
        with open("video.mp4", "wb") as f:
            f.write(res.content)
        res = requests.get(url.replace("d.dd", "www.dd"))
        soup = BeautifulSoup(res.text, "html.parser")
        description = soup.find_all("meta", property="og:description")[0]['content']
        return description

    def download_photo(self):
        url = self.url.replace("www.", "d.dd")
        res = requests.get(url)
        with open("image.png", "wb") as f:
            f.write(res.content)
        res = requests.get(url.replace("d.dd", "www.dd"))
        soup = BeautifulSoup(res.text, "html.parser")
        description = soup.find_all("meta", property="og:description")
        return description[0]['content']

import aiohttp
from bs4 import BeautifulSoup
import asyncio
from yarl import URL


class InstagramV2:
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
            print(soup)
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
                print(image_path)
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
