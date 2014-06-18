from scraper import search_CL
from scraper import read_search_results
from scraper import parse_source
from scraper import extract_listings
from scraper import fetch_json_results
from scraper import read_json_results
from scraper import add_location
from types import GeneratorType
import bs4


def test_search_CL():
    test_body, test_encoding = search_CL(minAsk=500, maxAsk=1000, bedrooms=2)
    assert "<span class=\"desktop\">craigslist</span>" in test_body
    assert test_encoding == 'utf-8'


def test_json_search():
    json = fetch_json_results()
    assert isinstance(json, list)
    assert isinstance(json[0], list)
    assert isinstance(json[0][0], dict)
    assert json[-1][u'baseurl'] == u'//seattle.craigslist.org'


def test_read_json():
    json = read_json_results()
    assert isinstance(json, list)
    assert isinstance(json[0], list)
    assert isinstance(json[0][0], dict)
    assert json[-1][u'baseurl'] == u'//seattle.craigslist.org'


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
    assert isinstance(test_data, GeneratorType)
    for dict_ in test_data:
        assert isinstance(dict_, dict)


def test_add_location_1():
    listing = {'pid': u'1'}
    search = {
        u'1': {'Latitude': 45.0, 'Longitude': 90.0},
        u'2': {'Latitude': 30.0, 'Longitude': 90.0}
    }
    assert add_location(listing, search) is True


def test_add_location_2():
    listing = {'pid': u'3'}
    search = {
        u'1': {'Latitude': 45.0, 'Longitude': 90.0},
        u'2': {'Latitude': 30.0, 'Longitude': 90.0}
    }
    assert add_location(listing, search) is False


def test_add_address():
    pass