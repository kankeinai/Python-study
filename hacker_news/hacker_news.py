import requests
from bs4 import BeautifulSoup
import pprint
import sys


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


def create_site(stories):
    with open('index.html', 'w') as site:
        site.write(
            "<!DOCTYPE html>\n<head>\n<title>Hacker news</title>\n<link href=\"style.css\" rel=\"stylesheet\" type=\"text/css\">\n<link href=\"https://fonts.googleapis.com/css2?family=Varta&display=swap\" rel=\"stylesheet\"></head>\n<body>\n<h1>Hacker news</h1>\n<table>")
        site.write("<tr><th>#</th><th>Title</th><th>Votes</th></tr>")
        i = 1
        for items in stories:
            site.write("<tr>")
            site.write(f"<td>{i}</td>\n")
            site.write(
                f"<td><a href=\"{items['link']}\">{items['title']}</a></td>\n")
            site.write(f"<td>{items['votes']}</td>\n")
            site.write("</tr>")
            i += 1
        site.write("</table>\n</body>")


def main(pages):
    stories = []
    stories = scan_pages(pages, stories)
    create_site(stories)
    return("Done.")


if __name__ == '__main__':
    sys.exit(main(int(sys.argv[1])))
