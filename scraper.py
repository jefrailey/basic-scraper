import requests
import os


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