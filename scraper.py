import requests
import os
from bs4 import BeautifulSoup
import sys


def search_CL(bedrooms=None, minAsk=None, maxAsk=None, query=None):
    url = "http://seattle.craigslist.org/search/apa"
    params = {}
    for k, v in locals().items():
        if v is not None:
            params[k] = v
    if not params:
        raise ValueError("No keywords given")
    else:
        response = requests.get(url, params=params)
    if response.ok:
        return response.content, response.encoding
    else:
        response.raise_for_status()

response, encoding = search_CL()
with open('apartments.html', 'w') as outfile:
    outfile.write(response)


def read_search_results(results='apartments.html'):
    with open(os.getcwd() + '/' + results, 'r') as source:
        return source.read(), 'utf-8'


def parse_source(body, encoding='utf-8'):
    return BeautifulSoup(body, from_encoding=encoding)


def extract_listings(parsed_html):
    listings = parsed_html.find_all('p', class_="row")
    data = []
    for listing in listings:
        link = listing.find('span', class_='pl').find('a')
        price = listing.find('span', class_='price')
        # price_span = listing.find('span', class_='price')
        size = price.next_sibling.strip('\n-/')
        this_listing = {
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price.string.strip(),
            'size': size
        }
        data.append(this_listing)
    return data


if __name__ == "__main__":
    import pprint
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        body, encoding = read_search_results()
    else:
        body, encoding = search_CL(minAsk=500, maxAsk=1000, bedrooms=2)
    parsed = parse_source(body, encoding)
    listings = extract_listings(parsed)
    print "Number of listings: {}".format(len(listings))
    pprint.pprint(listings[0])
