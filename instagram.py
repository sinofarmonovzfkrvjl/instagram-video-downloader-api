import requests

class Instagram:
    def __init__(self, url: str):
        self.url = url
    
    def download_video(self):
        url = self.url.replace("www.", "d.dd")
        res = requests.get(url)
        with open("video.mp4", "wb") as f:
            f.write(res.content)
        return True

    def download_photo(self):
        url = self.url.replace("www.", "d.dd")
        res = requests.get(url)
        with open("image.png", "wb") as f:
            f.write(res.content)
        return True


print(Instagram("https://www.instagram.com/reel/C_QZqjFpaMr/?utm_source=ig_web_copy_link").download_video())