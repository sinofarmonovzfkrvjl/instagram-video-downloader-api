import requests
from bs4 import BeautifulSoup

class InstagramV1:
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
    