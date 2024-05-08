import os
import uuid
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from newspaper import Article
from typing import Tuple

from urllib3 import Retry

load_dotenv("./.env")

SG_NEWS_API_KEY = os.getenv("SG_NEWS_API_KEY")
HEADERS = {
    # Google Chrome user agent header
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'hl':  'en'
}


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


def get_cna_article(temp_dir: str, target_url: str = ""):
    # s = requests.Session()
    # s.headers.update(HEADERS)
    # retry = Retry(connect=3, backoff_factor=0.5)  # type: ignore
    # adapter = HTTPAdapter(max_retries=retry)
    # s.mount('http://', adapter)
    # s.mount('https://', adapter)

    # r = s.get("https://www.channelnewsasia.com/singapore")

    print(target_url)

    def get_article_text_img(link: str):
        text = ""
        img_urls = []

        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'lxml')

        hero_section = soup.find("section", class_="detail-hero-media")
        if hero_section is not None:
            main_img = hero_section.find("img")
            img_urls.append(main_img['src'])  # type: ignore

        for article_div in soup.find_all("div", class_="content-wrapper"):
            # Section for related articles -> ignore
            if article_div.find("div", class_="referenced-card") is not None:
                continue

            # Section for social media -> ignore
            if article_div.find("div", class_="social-media") is not None:
                continue

            # TODO: potential use in video
            # Section for videos -> ignore
            if article_div.find("div", class_="video") is not None:
                continue

            if article_div.find("p") is not None:
                # Text Section
                for p in article_div.find_all("p"):
                    text += p.get_text()
            elif article_div.find("img") is not None:
                # Image Section
                for img in article_div.find_all("img"):
                    img_urls.append(img['src'])

        return (text, img_urls)

    article_url = ""

    CNA_URL = "https://www.channelnewsasia.com/singapore"
    CNA_BASE_URL = "https://www.channelnewsasia.com"

    if target_url == "":
        r = requests.get(CNA_URL)
        soup = BeautifulSoup(r.text, 'lxml')
        article_elements = soup.find_all(
            "div", class_="top-stories-primary-section__item")
        for article_element in article_elements:
            anchor_element = article_element.find('a', class_='link')
            href = anchor_element['href']
            if '/commentary' in href:
                continue
            article_url = CNA_BASE_URL + href
            break
    else:
        article_url = target_url

    print(article_url)
    text, img_urls = get_article_text_img(article_url)

    img_paths = []
    for img_url in img_urls:
        img_data = requests.get(img_url).content
        img_path = f"{temp_dir}/{uuid.uuid4()}.jpg"
        img_paths.append(img_path)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)

    return (text, img_paths)
