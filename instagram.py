import requests

url = input("Enter Video URL: ")
url = url.replace("instagram", "ddinstagram")
res = requests.get(url)
print(res.content)