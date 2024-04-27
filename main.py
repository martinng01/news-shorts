from footage import *
from gpt import *
from voice import *
from editor import *
from bot import *
from news import *
from captions import *

TEMP_DIR = "./tmp"


def generate_video(article: str, top_image: str, send_video_flag: bool = False):
    """
    This function generates a video from an article.
    It generates a script, search terms, voiceover, stock footage, and combines them into a video.


    Args:
        article (str): The article to generate the video from.
    """

    # Generate script
    script = generate_script(article, 3)
    print(f"Script: {script}")

    # Generate search terms
    search_terms = generate_search_terms(script, 6)
    print(f"Search terms: {search_terms}")

    # Generate voiceover
    voiceover = tts("en_au_001", script, TEMP_DIR)

    # Generate captions
    captions = generate_captions(voiceover, script, TEMP_DIR)

    # Change top image into a video
    image_video = image_to_video(top_image, 10)

    # Get stock footage for each search term
    video_paths = []
    for search_term in search_terms:
        print(f"Getting footage for search term {search_term}...", end="")
        stock_footage = get_stock_footage(search_term, 1, 5)
        if stock_footage is None or stock_footage == []:
            print(" No footage found.")
            continue
        video_path = download_footage(stock_footage[0], TEMP_DIR)
        video_paths.append(video_path)
        print(" Done!")

    videos = [VideoFileClip(path) for path in video_paths]
    videos = [image_video] + videos
    resized_videos = [resize_footage(video, (320, 480)) for video in videos]

    combined_video = combine_footage(
        resized_videos, AudioFileClip(voiceover).duration)
    combined_video = add_audio(combined_video, AudioFileClip(voiceover))
    combined_video = burn_captions(
        combined_video, captions, fontsize=28, stroke_width=2)
    combined_video = change_video_speed(combined_video, 1)

    final_video_path = write_video(combined_video, TEMP_DIR)

    # Send video
    if send_video_flag:
        print("Sending video...", end="")
        send_video(final_video_path)
        print(" Done!")


if __name__ == "__main__":
    article, top_image = get_singapore_article(TEMP_DIR)

    generate_video(article, top_image, False)
