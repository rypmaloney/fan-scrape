import pytest
import requests
import requests_mock
from scrape import get_all_pages


@requests_mock.Mocker(kw="mock")
def test(**kwargs):
    kwargs["mock"].get("http://123-fake-api.com", text="Hello!")

    response = requests.get("http://123-fake-api.com")


@requests_mock.Mocker(kw="mock")
def test_get_all_pages(**kwargs):
    wiki_id = "test_wiki"
    api_url = f"https://{wiki_id}.fandom.com/api/v1/Articles/List?limit=100"
    page_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    kwargs["mock"].get(
        api_url, json={"items": [{"id": page_id} for page_id in page_ids[:5]]}
    )
    kwargs["mock"].get(
        f"{api_url}",
        json={"items": [{"id": page_id} for page_id in page_ids]},
    )

    assert get_all_pages(wiki_id) == page_ids


@requests_mock.Mocker(kw="mock")
def test_get_all_pages_empty_response(**kwargs):
    wiki_id = "test_wiki"
    api_url = f"https://{wiki_id}.fandom.com/api/v1/Articles/List?limit=100"

    kwargs["mock"].get(api_url, json={})

    assert get_all_pages(wiki_id) == []
