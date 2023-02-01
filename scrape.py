import os
import json
import fandom
import requests
from tqdm import tqdm

from postgres_helpers import insert_page
from jdb_classes import FandomDatabase, FandomPage


def get_all_pages(wiki_id):
    """
    Fetches all pages of a Fandom wiki.

    This function uses the Fandom API to retrieve a list of pages in a wiki. The function returns the ID of each page in the wiki. The API call is repeated until all pages have been retrieved.

    Parameters:

    wiki_id (str): the id of the wiki to retrieve pages from.
    limit (int, optional): maximum number of pages to retrieve per API call. Default is 100.
    Returns:

    list: list of page IDs.
    """
    api_url = f"https://{wiki_id}.fandom.com/api/v1/Articles/List?limit=100"
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


def scrape():
    """
    Pulls all pages from a Fandom wiki and stores three ways:
    1. txt file with word:summary pair to be converted into a dictionary.
    2. Json file for further processing.
    3. Postgres databse. I'd rather not have to make repeat calls to the Fandom API.
    """
    fandom.set_wiki("wot")

    print("Pulling all pages...")
    all_pages = get_all_pages("wot")

    print("Initializing database...")
    database = FandomDatabase("data")

    print("Inserting page data....")
    cwd = os.getcwd()

    txt_location = os.path.join(cwd, "data", "dictionary.txt")
    with open(txt_location, "w") as file:

        for page_id in tqdm(all_pages):

            wrapped_page = fandom.page(pageid=page_id)
            data = wrapped_page.content

            # 1. Add to json database
            db_page = FandomPage(database, page_id)
            db_page.set_content(data)

            # 2. Add to Postgres database
            if "sections" in data:
                sections = json.dumps(data["sections"], indent=4)
            else:
                sections = None
            insert_page(page_id, data["title"], data["content"], sections)

            # 3. Add to txt file
            defintion = data["content"]
            definition = defintion.replace("\n", " ").replace("\r", " ")
            word_defintion = f"{data['title']}:{definition}"

            file.write(word_defintion + "\n")
