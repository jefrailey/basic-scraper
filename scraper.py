import requests
import os
from bs4 import BeautifulSoup
import sys
import json


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
        raise ValueError(u"No keywords given")
    else:
        response = requests.get(url, params=params)
    if response.ok:
        return response.content, response.encoding
    else:
        response.raise_for_status()


def fetch_json_results(**kwargs):
    u"""
    Return content of a response to a json query of CL.

    Submits a request to http://seattle.craigslist.org/jsonsearch/apa as
    search paramaters and returns the content of the
    server's response.  The search arguments need to match
    search_CL()'s in order for this to collect the corresponding data.

    Keyword arguments:
    bedrooms: An int indicating the minimum number of bedrooms.
    minAsk: An int indicating the minimum monthly rent.
    maxAsk: An int indicating the maximum monthly rent.
    query: A string representing other search terms 'parking', 'bus', etc.
    """
    url = 'http://seattle.craigslist.org/jsonsearch/apa'
    results = requests.get(url, params=kwargs)
    results.raise_for_status()
    return results.json()


def read_search_results(results='apartments.html'):
    u"""Return the contents of a local html file."""
    with open(os.getcwd() + '/' + results, 'r') as source:
        return source.read(), 'utf-8'


def read_json_results(results='apartments.json'):
    u"""Return the contents of a local json file."""
    with open(os.getcwd() + '/' + results, 'r') as source:
        json_string = source.read()
        return json.loads(json_string)


def parse_source(body, encoding='utf-8'):
    u"""Return HTML parsed by BeautifulSoup."""
    return BeautifulSoup(body, from_encoding=encoding)


def extract_listings(parsed_html):
    u"""
    Yield list of dicts containing attributes of listed apartments.

    Accepts BeautifulSoup parsed HTML.  Searches and traverses
    the parsed HTML for each listing and collects the link to,
    description of, price, and size of each apartment.

    Yield:
    Dictionary containing apartment attributes.
    """
    listings = parsed_html.find_all('p', class_="row")
    for listing in listings:
        link = listing.find('span', class_='pl').find('a')
        price = listing.find('span', class_='price')
        size = price.next_sibling.strip('\n-/')
        this_listing = {
            'pid': listing.attrs.get('data-pid', ''),
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price.string.strip(),
            'size': size
        }
        yield this_listing


def add_location(listing, search):
    u"""
    Merge latt/long search results into the listing's dictionary.

    Accepts a dictionary representing a listing on CL and adds the
    lattitude and longitude specificed for that listing in a
    CL JSON search.

    Return:
    True: If listing's identifier (pid) is in the search output.
    False: If listing's identifier (pid) is not in the search output.
    """
    if listing['pid'] in search:
        match = search[listing['pid']]
        listing['location'] = {
            'data-latitude': match.get('Latitude', ''),
            'data-longitude': match.get('Longitude', '')
        }
        return True
    return False


def add_address(listing):
    u"""
    Return the listing with an address from Google Maps based on lat/long.

    Return:
    Dictionary with a new key, 'address', that ncludes the an address for the
    listing's lat/long if it can be determined or the string 'unavailable' if
    it can't.
    """
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    latlng = "{data-latitude},{data-longitude}".format(**listing['location'])
    parameters = {'latlng': latlng, 'sensor': 'false'}
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()
    if data['status'] == 'OK':
        best = data['results'][0]
        listing['address'] = best['formatted_address']
    else:
        listing['address'] = 'unavailable'
    return listing


if __name__ == "__main__":
    import pprint
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        response, encoding = read_search_results()
        json_res = read_json_results()
    else:
        response, encoding = search_CL(minAsk=1000, maxAsk=1500, bedrooms=2)
        with open('apartments.html', 'w') as outfile:
            outfile.write(response)
        json_res = fetch_json_results(minAsk=1000, maxAsk=1500, bedrooms=2)
        with open('apartments.json', 'w') as outfile:
            outfile.write(json.dumps(json_res))
    parsed = parse_source(response, encoding)
    search = {j['PostingID']: j for j in json_res[0]}
    for listing in extract_listings(parsed):
        if (add_location(listing, search)):
            listing = add_address(listing)
            pprint.pprint(listing)
