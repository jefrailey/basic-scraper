import requests
import os
from bs4 import BeautifulSoup
import sys


def search_CL(bedrooms=None, minAsk=None, maxAsk=None, query=None):
    u"""
    Return content and encoding of a response to a query of CL.

    Submits a request to http://seattle.craigslist.org/search/apa as
    search paramaters and returns the content and encoding of the
    server's response.

    Keyword arguments:
    bedrooms: An int indicating the minimum number of bedrooms.
    minAsk: An int indicating the minimum monthly rent.
    maxAsk: An int indicating the maximum monthly rent.
    query: A string representing other search terms 'parking', 'bus', etc.
    """
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


def read_search_results(results='apartments.html'):
    u"""Returns the contents of a local html file."""
    with open(os.getcwd() + '/' + results, 'r') as source:
        return source.read(), 'utf-8'


def parse_source(body, encoding='utf-8'):
    u"""Return HTML parsed by BeautifulSoup."""
    return BeautifulSoup(body, from_encoding=encoding)


def extract_listings(parsed_html):
    u"""
    Return list of dicts containing attributes of listed apartments.

    Accepts BeautifulSoup parsed HTML.  Searches and traverses
    the parsed HTML for each listing and collects the link to,
    description of, price, and size of each apartment.  These values
    are returned in a list that contains one dictionary per apartment.
    """
    listings = parsed_html.find_all('p', class_="row")
    data = []
    for listing in listings:
        link = listing.find('span', class_='pl').find('a')
        price = listing.find('span', class_='price')
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
        body, encoding = search_CL(minAsk=1000, maxAsk=1500, bedrooms=2)
        response, encoding = search_CL()
        with open('apartments.html', 'w') as outfile:
            outfile.write(response)
    parsed = parse_source(body, encoding)
    listings = extract_listings(parsed)
    print "Number of listings: {}".format(len(listings))
    pprint.pprint(listings[0])
