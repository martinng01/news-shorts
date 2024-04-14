from footage import *
from gpt import *
from voice import *
from video import *
from bot import *
from news import *

TEMP_DIR = "./tmp"


def generate_video(article: str, send_video_flag: bool = False):
    """
    This function generates a video from an article.
    It generates a script, search terms, voiceover, stock footage, and combines them into a video.


    Args:
        article (str): The article to generate the video from.
    """

    script = generate_script(article, 3)
    search_terms = generate_search_terms(script, 3)
    voiceover = tts("en_au_001", script, TEMP_DIR)

    video_paths = []
    print(search_terms)
    for search_term in search_terms:
        stock_footage = get_stock_footage(search_term, 1, 5)[0]
        video_path = download_footage(stock_footage, TEMP_DIR)
        video_paths.append(video_path)

    combined_video = combine_resize_footage(
        video_paths, AudioFileClip(voiceover).duration, TEMP_DIR)
    final_video = add_audio(combined_video, voiceover, TEMP_DIR)

    if send_video_flag:
        send_video(final_video)


if __name__ == "__main__":
    article = get_article()

    generate_video(article, False)
