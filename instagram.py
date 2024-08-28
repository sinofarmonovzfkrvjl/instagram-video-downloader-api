import requests
from bs4 import BeautifulSoup


class Instagram:
    def __init__(self, url):
        self.url = url
    
    def download_video(self):
        url = self.url
        video = url.replace("www.", "d.dd")
        res = requests.get(video)
        with open("video.mp4", 'wb') as video:
            video.write(res.content)
        
    def download_photo(self):
        url = self.url
        video = url.replace("www.", "d.dd")
        res = requests.get(video)
        with open("image.png", 'wb') as video:
            video.write(res.content)
