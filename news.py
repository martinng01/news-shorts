import os
from dotenv import load_dotenv
import requests
from newspaper import Article
from typing import Tuple

load_dotenv("./.env")

SG_NEWS_API_KEY = os.getenv("SG_NEWS_API_KEY")


def get_singapore_article() -> Tuple[str, str]:
    """
    Fetches the first article from the top headlines in Singapore.

    Returns:
    Tuple[str, str]: The article text and the top image
    """

    news_outlets = ["The Straits Times", "CNA", "TODAY"]

    response = requests.get("https://newsapi.org/v2/top-headlines", params={
        "country": "sg", "apiKey": SG_NEWS_API_KEY})

    json = response.json()

    articles = list(
        filter(lambda article: article["author"] in news_outlets, json["articles"]))
    article = Article(url=articles[0]['url'])
    article.download()
    article.parse()

    # TODO Utilise top image
    return (article.text, article.top_image)


# get_singapore_article()
