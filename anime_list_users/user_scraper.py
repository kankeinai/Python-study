from selenium import webdriver
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os


path = "/Users/milanabegantsova/Documents/GitHub/anime_info_searcher/chromedriver"
driver = webdriver.Chrome(path)


def get_links(page):
    links = set()
    url = 'https://yummyanime.club/reviews?page=' + str(page)
    response = Request(url, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(response, timeout=20).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    tags = soup.findAll(
        'a', {'class': 'small-text'})
    for item in tags:
        links.add('https://yummyanime.club/users/id' +
                  item['href'].split('=')[-1])
    return list(links)


def clear_title(title):
    return ' '.join(title.split())


def save_data(elements):
    anime = []
    for item in elements:
        soup = BeautifulSoup(item.get_attribute('innerHTML'), 'html.parser')
        title = clear_title(
            (soup.find('span', {'class': 'update-title'})).getText())
        try:
            rates = int(
                (soup.find('span', {'class': 'user-rating'})).getText().replace(" ", ''))
        except:
            continue
        anime.append({'anime': title, 'rate': rates})
    print(anime)
    return anime


def main():
    folder = 'users/'
    if os.path.exists(folder) == False:
        os.mkdir(folder)
    page = 86
    while page > 0:
        print(page)
        links = get_links(page)
        for url in links:
            driver.get(url)
            user_id = url.split('/')[-1]
            filename = folder + user_id + '.csv'
            if os.path.exists(filename) == False:
                try:
                    button = driver.find_element_by_xpath(
                        '//li[@data-id="#watched"]')
                    button.click()
                    sleep(5)
                    elements = driver.find_elements_by_class_name(
                        'update-list-block')
                    anime = save_data(elements)
                    if len(anime) >= 15:
                        df = pd.DataFrame.from_dict(anime)
                        df.to_csv('users/' + user_id + '.csv',
                                  sep=',', encoding='utf-8-sig')
                except:
                    pass
        page -= 1

    driver.quit()


if __name__ == "__main__":
    main()
