basic-scraper
=============

This module contains functions designed to scrape Seattle apartment listings on Craigslist as outlined in [this tutorial](http://codefellows.github.io/python-dev-accelerator/assignments/day11/scraper.html).
It uses [Requests](http://docs.python-requests.org/en/latest/) to obtain the HTML and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) to parse it.

When ran, the module will search for two bedroom apartments with a monthly rent between
$1000 and $1500 per month. It will save the searches as 'apartment.html' and 'apartments.json' If the optional 'test' argument is called:

    $ python scraper.py test

the scraper will read in the 'apartment.html' file instead of sending a new request to Craigslist.


    search_CL(bedrooms=None, minAsk=None, maxAsk=None, query=None)
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

    fetch_json_results(**kwargs):
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

    read_search_results(results='apartments.html')
        u"""Returns the contents of a local html file."""

    read_json_results(results='apartments.json'):
        u"""Return the contents of a local json file."""

    parse_source(body, encoding='utf-8')
        u"""Return HTML parsed by BeautifulSoup."""

    extract_listings(parsed_html)
        u"""
        Yield list of dicts containing attributes of listed apartments.

        Accepts BeautifulSoup parsed HTML.  Searches and traverses
        the parsed HTML for each listing and collects the link to,
        description of, price, and size of each apartment.

        Yield:
        Dictionary containing apartment attributes.
        """

    add_location(listing, search):
        u"""
        Merge latt/long search results into the listing's dictionary.

        Accepts a dictionary representing a listing on CL and adds the
        lattitude and longitude specificed for that listing in a
        CL JSON search.

        Return:
        True: If listing's identifier (pid) is in the search output.
        False: If listing's identifier (pid) is not in the search output.
        """

    def add_address(listing):
        u"""
        Return the listing with an address from Google Maps based on lat/long.

        Return:
        Dictionary with a new key, 'address', that ncludes the an address for the
        listing's lat/long if it can be determined or the string 'unavailable' if
        it can't.
        """