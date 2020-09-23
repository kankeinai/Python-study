from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from urllib.request import Request, urlopen
from time import sleep
from urllib.parse import quote
from email_sender import notify


def anime_loader(first_page, last_page):
    anime = []
    for i in range(first_page, last_page+1):
        print(f"Страница #{i}")
        url = 'https://yummyanime.club/filter?selected_type%5B0%5D=7&status=-1&season=0&selected_age=0&sort=1&action=1&page=' + \
            str(i)
        response = Request(url, headers={'User-Agent': 'XYZ/3.0'})
        webpage = urlopen(response, timeout=20).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        links = soup.findAll(
            'a', {'class': 'anime-title'})
        hrefs = []
        names = []
        for link in links:
            hrefs.append('https://yummyanime.club' + quote(link['href']))
            names.append(link.getText())
        for idx, url in enumerate(hrefs):
            try:
                sleep(0.7)
                response = Request(url,
                                   headers={'User-Agent': 'XYZ/3.0'})
                webpage = urlopen(response, timeout=20).read()
                soup = BeautifulSoup(webpage, 'html.parser')
                type_anime = (
                    soup.find('li', {'id': 'animeType'}).getText()).replace('Тип: ', '').replace('\n', '').split(' ')[0]
                print(type_anime)
                if type_anime == 'ONA':
                    try:
                        img = 'https://yummyanime.club'+(soup.find('div', {'class': 'poster-block'})
                                                         ).find('img').get('src')
                    except:
                        img = None
                    try:
                        rate = (
                            soup.find('span', {'class': 'main-rating'})).getText()
                    except:
                        rate = None
                    try:
                        votes = (soup.find('span', {'class': 'main-rating-info'})
                                 ).getText().replace(' голосов)', '').replace('(', '')
                    except:
                        votes = None

                    categories = soup.findAll(
                        'li', {'class': 'categories-list'})
                    genres = []
                    genre = categories[0].findAll('a')
                    for item in genre:
                        genres.append(item.getText().replace('\n', ''))
                    try:
                        studio = categories[1].find('a').getText()
                    except:
                        studio = None
                    try:
                        producer = categories[2].find('li').getText()
                    except:
                        producer = None
                    main_info = soup.find(
                        'ul', {'class': 'content-main-info'}).findAll('li', {})
                    keys = []
                    values = []
                    for line in main_info:
                        key = line.find('span').getText().split(':')[0]
                        if key == 'Жанр':
                            break
                        else:
                            keys.append(key)
                            values.append(line.getText().split(':')
                                          [1].replace('\n', ''))
                    anime_info = dict(zip(keys, values))
                    try:
                        anime_info['Возрастной рейтинг'] = (
                            anime_info['Возрастной рейтинг'][1:]).split(' ')[0]
                    except:
                        anime_info['Возрастной рейтинг'] = None
                    description = ''
                    desc = soup.find(
                        'div', {'id': 'content-desc-text'}).findAll('p')
                    for paragraph in desc:
                        description += paragraph.getText()
                    try:
                        result = {'name': names[idx], 'description': description.replace('\n', ''), 'img': img,
                                  'rate': rate, 'votes': votes, 'genres': genres, 'studio': studio, 'watches': anime_info['Просмотров'], 'year': anime_info['Год'], 'season': anime_info['Сезон'].replace(' ', ''), 'age': anime_info['Возрастной рейтинг']}
                        print(result)
                        anime.append(result)
                    except:
                        pass
                else:
                    pass
            except:
                pass
    return anime


first_page = 1
last_page = 6
anime = anime_loader(first_page, last_page)
df = pd.DataFrame.from_dict(anime)
df.to_csv('ona' + str(first_page) + '-'+str(last_page) +
          '.csv', sep=',', encoding='utf-8-sig')
notify(first_page, last_page)
