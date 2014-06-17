from scraper import search_CL
from scraper import read_search_results


def test_search_CL():
    test_body, test_encoding = search_CL(minAsk=100)
    assert "<span class=\"desktop\">craigslist</span>" in test_body
    assert test_encoding == 'utf-8'


def test_read_search_result():
    test_body, test_encoding = read_search_results()
    assert "<span class=\"desktop\">craigslist</span>" in test_body
    assert test_encoding == 'utf-8'
