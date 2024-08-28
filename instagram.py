import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import instaloader
import glob
import os


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
                
        
print(Instagram("https://www.instagram.com/p/C_MwyEANzlZ/?utm_source=ig_web_copy_link&").download_photo())