from bot import send_video
from main import generate_video
from news import get_cna_article

TEMP_DIR = "tmp"


def lambda_handler(event, context):
    article_dict = get_cna_article(
        TEMP_DIR, target_url="")
    print(article_dict['title'])
    video_path = generate_video(
        article_dict['text'], article_dict['img_paths'])

    send_video(video_path=video_path,
               link=article_dict['link'],
               title=article_dict['title'],
               desc=article_dict['desc'])
