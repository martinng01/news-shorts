import os
import uuid
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

load_dotenv("./.env")


def get_cna_article(temp_dir: str, target_url: str = ""):
    print(target_url)

    def get_article_text_img(link: str):
        title = ""
        text = ""
        desc = ""
        img_urls = []

        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'lxml')

        h1 = soup.find("h1", class_="h1--page-title")
        if h1 is not None:
            title = h1.get_text().strip()

        desc_tag = soup.find("div", class_="content-detail__description")
        if desc_tag is not None:
            p = desc_tag.find("p")
            desc = p.get_text().strip() if p is not None else ""  # type: ignore

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

            # Section for social media -> ignore
            if article_div.find("div", class_="embed") is not None:
                continue

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

        return {"title": title, "text": text, "img_urls": img_urls, "desc": desc}

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
    res = get_article_text_img(article_url)
    text = res['text']
    img_urls = res['img_urls']
    title = res['title']
    desc = res['desc']

    img_paths = []
    for img_url in img_urls:
        img_data = requests.get(img_url).content
        img_path = os.path.join(temp_dir, f"{uuid.uuid4()}.jpg")
        img_paths.append(img_path)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)

    return {"text": text, "img_paths": img_paths, "title": title, "link": article_url, "desc": desc}
