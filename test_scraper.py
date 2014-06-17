from scraper import search_CL
from scraper import read_search_results
from scraper import parse_source
from scraper import extract_listings
import bs4


def test_search_CL():
    test_body, test_encoding = search_CL(minAsk=500, maxAsk=1000, bedrooms=2)
    assert "<span class=\"desktop\">craigslist</span>" in test_body
    assert test_encoding == 'utf-8'


def test_read_search_result():
    test_body, test_encoding = read_search_results()
    assert "<span class=\"desktop\">craigslist</span>" in test_body
    assert test_encoding == 'utf-8'


def test_parse_source():
    test_body, test_encoding = read_search_results()
    test_parse = parse_source(test_body, test_encoding)
    assert isinstance(test_parse, bs4.BeautifulSoup)


def test_extract_listings():
    test_body, test_encoding = read_search_results()
    test_parse = parse_source(test_body, test_encoding)
    test_data = extract_listings(test_parse)
    assert isinstance(test_data, list)
    for dict_ in test_data:
        assert isinstance(dict_, dict)