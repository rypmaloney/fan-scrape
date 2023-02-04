import os
import time
import json
import fandom
import requests
from tqdm import tqdm

from postgres_helpers import insert_page, connect
from jdb_classes import FandomDatabase, Page


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


def process_page_data(wrapped_page, page_id, json_db, text_file):
    data = wrapped_page.content

    # 1. Add to json database
    db_page = Page(json_db, page_id)
    db_page.set_content(data)

    # 2. Add to Postgres database
    sections = json.dumps(data.get("sections", None))
    insert_page(page_id, data["title"], data["content"], sections)

    # 3. Add to txt file
    defintion = data["content"]
    definition = defintion.replace("\n", " ").replace("\r", " ")
    word_definition = f"{data['title']}:{definition}"
    if not any(  # skip not useful entries
        word in data["title"]
        for word in [
            "chapter",
            "Chapter",
            "Timeline",
            "timeline",
            "NE",
        ]
    ):
        text_file.write(word_definition + "\n")


def scrape(wiki_name, data_dir):
    """
    Pulls all pages from a Fandom wiki and stores three ways:
    1. txt file with word:summary pair to be converted into a dictionary.
    2. Json file for further processing.
    3. Postgres database for persistent storage.

    Parameters:
    wiki_name (str): Name of the Fandom wiki to scrape.
    data_dir (str): Directory to store the scraped data.
    """
    fandom.set_wiki(wiki_name)

    print("Pulling all pages...")
    all_pages = get_all_pages(wiki_name)

    database = FandomDatabase(data_dir)
    cwd = os.getcwd()
    txt_location = os.path.join(cwd, data_dir, "dictionary.txt")

    with open(txt_location, "w") as file:

        for page_id in tqdm(all_pages):
            # Added rate limiting and retries
            max_retries = 5
            retry_wait_time = 60
            retries = 0

            while True:
                try:
                    wrapped_page = fandom.page(pageid=page_id)
                    tqdm.write(wrapped_page.title)

                    process_page_data(wrapped_page, page_id, database, file)
                    break

                except Exception:
                    retries += 1
                    if retries > max_retries:
                        tqdm.write(f"Too many retries, giving up on {page_id}")
                        break
                    tqdm.write("Waiting to retry...")
                    time.sleep(retry_wait_time)
