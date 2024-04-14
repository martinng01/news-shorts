from main import generate_video
from news import get_article


def lambda_handler(event, context):
    article = get_article()
    generate_video(article, True)
