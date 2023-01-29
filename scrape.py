import fandom
import requests
from tqdm import tqdm

from db_models import FandomDatabase, FandomPage


def get_all_pages(wiki_id, limit=100):
    api_url = f"https://{wiki_id}.fandom.com/api/v1/Articles/List?limit={limit}"
    all_pages = []
    offset = ""
    while True:
        response = requests.get(f"{api_url}&offset={offset}", timeout=10)
        data = response.json()
        pages = data.get("items", [])

        if not pages:
            break

        all_pages.extend([page["id"] for page in pages])

        try:
            offset = data["offset"]
        except KeyError:
            break
    return all_pages


def create_content():
    fandom.set_wiki("wot")

    print("Pulling all pages...")
    all_pages = get_all_pages("wot")

    print("Initializing database...")
    database = FandomDatabase("data")

    print("Inserting page data....")
    for page_id in tqdm(all_pages):
        wrapped_page = fandom.page(pageid=page_id)
        db_page = FandomPage(database, page_id)

        db_page.set_content(wrapped_page.content)
