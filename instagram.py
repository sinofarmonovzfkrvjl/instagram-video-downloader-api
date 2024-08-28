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
        # image = url.replace("www.", "d.dd")
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        # with open("image.png", 'wb') as video:
        #     video.write(res.content)
        return soup.find_all("img", attrs={'class': 'x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'})
        
        
print(Instagram("https://www.instagram.com/p/C_MwyEANzlZ/?utm_source=ig_web_copy_link&img_index=1").download_photo())