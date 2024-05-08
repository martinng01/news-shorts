import os
import uuid
from dotenv import load_dotenv
import requests
from newspaper import Article
from typing import Tuple

load_dotenv("./.env")

SG_NEWS_API_KEY = os.getenv("SG_NEWS_API_KEY")


def get_singapore_article(path: str) -> Tuple[str, str]:
    """
    Fetches the first article from the top headlines in Singapore.

    Returns:
    Tuple[str, str]: The article text and the top image
    """

    news_outlets = ["The Straits Times", "CNA", "TODAY"]

    response = requests.get("https://newsapi.org/v2/top-headlines", params={
        "country": "sg", "category": "general", "apiKey": SG_NEWS_API_KEY})

    json = response.json()

    articles = list(
        filter(lambda article: article["author"] in news_outlets, json["articles"]))
    print(articles[0]['url'])
    article = Article(url=articles[0]['url'])
    article.download()
    article.parse()

    # Download top image to temp dir
    img_data = requests.get(article.top_image).content
    img_path = f"{path}/{uuid.uuid4()}.jpg"
    with open(img_path, 'wb') as img:
        img.write(img_data)

    return (article.text, img_path)


# get_singapore_article()
