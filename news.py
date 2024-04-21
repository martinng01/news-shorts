import os
from dotenv import load_dotenv
import requests

load_dotenv("./.env")

THEGUARDIAN_API_KEY = os.getenv("THEGUARDIAN_API_KEY")
API_ENDPOINT = 'http://content.guardianapis.com/search'
params = {
    "section": "world",
    "order-by": "newest",
    "page-size": 10,
    "show-fields": "bodyText",
    "api-key": THEGUARDIAN_API_KEY,
}


def get_article() -> str:
    """
    Fetches the first article from The Guardian API.

    Returns:
    str: The article text
    """

    response = requests.get(API_ENDPOINT, params)
    if response.status_code != 200:
        print("Error fetching articles from The Guardian")
        print(response.text)

    results_json_list = response.json(
    )['response']['results']

    # Get the first result labeled as an article
    article_json = next(
        filter(lambda x: x['type'] == 'article', results_json_list))

    print(article_json['webUrl'])

    return article_json['fields']['bodyText']
