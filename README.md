basic-scraper
=============

This module contains functions designed to scrape Seattle apartment listings on Craigslist.
It uses [Requests](http://docs.python-requests.org/en/latest/) to obtain the HTML and [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) to parse it.

When ran, the module will search for two bedroom apartments with a monthly rent between
$1000 and $1500 per month. It will save this search as 'apartment.html.' If the optional 'test' argument is called:

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

    read_search_results(results='apartments.html')
        u"""Returns the contents of a local html file."""

    parse_source(body, encoding='utf-8')
        u"""Return HTML parsed by BeautifulSoup."""

    extract_listings(parsed_html)
        u"""
        Return list of dicts containing attributes of listed apartments.

        Accepts BeautifulSoup parsed HTML.  Searches and traverses
        the parsed HTML for each listing and collects the link to,
        description of, price, and size of each apartment.  These values
        are returned in a list that contains one dictionary per apartment.
        """
