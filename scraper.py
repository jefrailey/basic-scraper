import requests


def search_CL(bedrooms=None, minAsk=None, maxAsk=None, query=None):
    url = "http://seattle.craigslist.org/search/apa"
    params = {}
    for k, v in locals().items():
        params[k] = v
    if not params:
        raise ValueError("No keywords given")
    else:
        response = requests.get(url, params=params)
    if response.ok:
        return response.text, response.encoding
    else:
        response.raise_for_status()

# output = search_CL()
# with open('apartments.html', 'w') as outfile:
#     outfile.write(output)
