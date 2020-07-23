

from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import time
from urllib.request import Request, urlopen
import urllib.request
from urllib.parse import quote
from PIL import Image


def save_image(name, url):
    image_name = name.replace(" ", "_") + ".jpg"
    folder = "images"
    if not os.path.exists(folder):
        os.mkdir(folder)
    if not os.path.isfile(folder + "/" + image_name):
        print("Downloading")
        urllib.request.urlretrieve(url, folder + "/" + image_name)
    return Image.open(folder + "/" + image_name)


def get_link(anime_name):
    print(anime_name)
    url = "https://shikimori.one/animes?search=" + \
        quote(anime_name.replace(" ", "+"))
    response = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(response, timeout=20).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    spans = soup.find_all('span', {'class': 'image-cutter'})
    img = spans[0].find('img')
    return img['srcset'].split(" ")[0]
