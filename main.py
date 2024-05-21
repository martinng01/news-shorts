from typing import List
from bot import send_video
from editor import image_to_video, resize_footage, combine_footage, burn_captions, write_video
from voice import generate_audio_aws
from news import get_cna_article
from footage import get_stock_footage, download_footage
from captions import generate_captions
from gpt import generate_script, generate_search_terms
from moviepy.editor import VideoFileClip, AudioFileClip
import os


TEMP_DIR = "tmp"


def generate_video(article: str, img_paths: List[str]):
    """
    This function generates a video from an article.
    It generates a script, search terms, voiceover, stock footage, and combines them into a video.


    Args:
        article (str): The article to generate the video from.
    """

    temp_paths = []

    # Generate script
    script = generate_script(article, 3)
    print(f"Script: {script}")

    # Generate search terms
    search_terms = generate_search_terms(script, 3)
    print(f"Search terms: {search_terms}")

    # Generate voiceover
    voiceover = generate_audio_aws(script, TEMP_DIR)
    temp_paths.append(voiceover)

    # Generate captions
    captions = generate_captions(voiceover, TEMP_DIR)
    temp_paths.append(captions)

    # Change top image into a video
    temp_paths.extend(img_paths)
    img_videos = [image_to_video(img_path, 5) for img_path in img_paths]

    # Get stock footage for each search term
    video_paths = []
    for search_term in search_terms:
        print(f"Getting footage for search term {search_term}...", end="")
        stock_footage = get_stock_footage(search_term, 2, 5)
        if stock_footage is None or stock_footage == []:
            print(" No footage found.")
            continue
        video_path = download_footage(stock_footage[0], TEMP_DIR)
        video_paths.append(video_path)
        print(" Done!")

    temp_paths.extend(video_paths)
    videos = [VideoFileClip(path) for path in video_paths]
    videos = img_videos + videos
    resized_videos = [resize_footage(video, (320, 480)) for video in videos]

    combined_video = combine_footage(
        resized_videos, AudioFileClip(voiceover).duration)
    combined_video = burn_captions(
        combined_video, captions, fontsize=22, stroke_width=1.5)
    combined_video = write_video(
        combined_video, voiceover, TEMP_DIR)

    # Cleanup tmp files
    for path in temp_paths:
        os.remove(path)

    return combined_video


if __name__ == "__main__":
    article_dict = get_cna_article(
        TEMP_DIR, target_url="")
    print(article_dict['title'])
    video_path = generate_video(
        article_dict['text'], article_dict['img_paths'])

    send_video(video_path=video_path,
               link=article_dict['link'],
               title=article_dict['title'],
               desc=article_dict['desc'])
