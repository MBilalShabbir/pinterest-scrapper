import requests
import re
from bs4 import BeautifulSoup
import urllib


def scraps(url):
    res = requests.get(url)
    # soup = BeautifulSoup(res.text, 'html.parser')

    videos = list(set(re.findall(r'https://[^"]+' + '[^"]+mp4', res.text)))
    images = list(set(re.findall(r'https://[^"]+' + '[^"]+jpg', res.text)))
    return {'images': images, 'videos': videos}
