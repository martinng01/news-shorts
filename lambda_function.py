from main import generate_video
from news import get_guardian_article


def lambda_handler(event, context):
    article = get_guardian_article()
    generate_video(article, True)
