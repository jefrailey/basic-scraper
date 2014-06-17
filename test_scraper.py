from scraper import search_CL
from scraper import read_search_results
from scraper import parse_source
from scraper import extract_listings
import bs4


def test_search_CL():
    test_body, test_encoding = search_CL(minAsk=100, maxAsk=100)
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
    for row in extract_listings(test_parse):
        print type(row)
        assert isinstance(row, bs4.element.Tag)
