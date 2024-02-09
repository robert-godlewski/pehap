# This is generally used to find links that I need for the research
# References: https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup


def findLink(soup: BeautifulSoup, id: str='', title: str='') -> str:
    tag = None
    if id != '':
        tag = soup.find(id=id)
    if title != '':
        tag = soup.find(title=title)
    if tag and tag.attrs['href']:
        # print(tag.name)
        # print(tag.attrs)
        baselink = tag['href']
        # print(baselink)
        linkarr = baselink.split("/")
        link = linkarr[len(linkarr)-1]
        return link
    else:
        return ''
