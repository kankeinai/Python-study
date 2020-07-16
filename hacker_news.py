import requests
from bs4 import BeautifulSoup
import pprint
import sys


def print_stories_hn(hnlist):
    i = 1
    for items in hnlist:
        print(
            f"{i}. {items['title']}\nLink: {items['link']}\nVotes: {items['votes']}\n")
        i += 1


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext, stories):
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().split(' ')[0])
            if points > 100:
                stories.append({'title': title, 'link': href, 'votes': points})


def scan_pages(pages, stories):
    for i in range(1,  pages):
        res = requests.get('https://news.ycombinator.com/news?p='+str(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        create_custom_hn(links, subtext, stories)
    return sort_stories_by_votes(stories)


def main(pages):
    stories = []
    stories = scan_pages(pages, stories)
    print_stories_hn(stories)
    return("Done.")


if __name__ == '__main__':
    sys.exit(main(int(sys.argv[1])))
