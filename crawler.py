# wiki_scraping.py

# python standart library
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import re

# third-party library
from bs4 import BeautifulSoup

# my library


def find_adjacent_links(bs):
    """
    this function finds related links in webpage 
    and return a set which has urls as elements to remove duplicate links 
    """

    result = set() 
    # /wiki/<string>    <string> doesn't include ':'
    pattern = re.compile('^(/wiki/)((?!:).)*$')

    try:
        div_component = bs.find('div', {'id': 'bodyContent'})
        for link in div_component.findAll('a', href=pattern):
            if 'href' in link.attrs:
                article = link.attrs['href']
                result.add('http://en.wikipedia.org{}'.format(article))
    # if there are no tags i look for this error occurs
    except AttributeError as err:
        print(err) # to be converted to log err later
    finally:
        return result

def travel_webpages(bs, visited):
    """
    this function randomly retrieve webpages in one website 
    """
    remains = set() 
    
    collect_info(bs)
    adj_links = find_adjacent_links(bs)
    # get adj_links not visited
    adj_links -= visited
    remains.update(adj_links)

    assert remains
    while remains:
        if adj_links:
            next_link = adj_links.pop()
        else:
            next_link = remains.pop()

        try:
            remains.remove(next_link)
            visited.add(next_link)
            with urlopen(next_link) as html:
                bs = BeautifulSoup(html.read(),'html.parser')
                print(next_link)
        except HTTPError as err:
            print(err) # to be converted to log err
        except URLError as err:
            print(err) # to be converted to log err
        else:
            collect_info(bs)
            adj_links = find_adjacent_links(bs)
            # get adj_links not visited
            adj_links -= visited
            remains.update(adj_links)



def collect_info(bs):
    print('happy coding')


def main():
    urls = ['http://en.wikipedia.org/wiki/Kevin_Bacon']
    visited = set()

    for url in urls:
        try:
            visited.add(url)
            with urlopen(url) as html:
                bs = BeautifulSoup(html.read(), 'html.parser')
        except HTTPError as err:
            print(err)
        except URLError as err:
            print(err)
        else:
            travel_webpages(bs, visited)
            print('conquer this website: {}'.format(url))


if __name__ == '__main__':
    main()
