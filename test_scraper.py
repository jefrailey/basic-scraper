from scraper import search_CL


def test_search_CL():
    test_body, test_encoding = search_CL(minAsk=100)
    assert "<span class=\"desktop\">craigslist</span>" in test_body
    assert test_encoding == 'utf-8'