import requests
from bs4 import BeautifulSoup
import instaloader


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
        post_url = self.url
        L = instaloader.Instaloader()
        post_shortcode = post_url.split("/")[-2]
        L.download_post(instaloader.Post.from_shortcode(L.context, post_shortcode), target=post_shortcode)