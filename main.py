from footage import *
from gpt import *
from voice import *
from editor import *
from bot import *
from news import *
from captions import *

TEMP_DIR = "./tmp"


def generate_video(article: str, send_video_flag: bool = False):
    """
    This function generates a video from an article.
    It generates a script, search terms, voiceover, stock footage, and combines them into a video.


    Args:
        article (str): The article to generate the video from.
    """

    # Generate script
    print("Generating script...", end="")
    script = generate_script(article, 3)
    print(" Done!")

    # Generate search terms
    print("Generating search terms...", end="")
    search_terms = generate_search_terms(script, 6)
    print(" Done!")
    print(f"Search terms: {search_terms}")

    # Generate voiceover
    print("Generating voiceover...", end="")
    voiceover = tts("en_au_001", script, TEMP_DIR)
    print(" Done!")

    # Generate captions
    print("Generating captions...", end="")
    captions = generate_captions(voiceover, TEMP_DIR)
    print(" Done!")

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
        print(video_path)
        print()

    videos = [VideoFileClip(path) for path in video_paths]
    resized_videos = [resize_footage(video, (320, 480)) for video in videos]

    print("Processing videos...", end="")
    combined_video = combine_footage(
        resized_videos, AudioFileClip(voiceover).duration)
    combined_video = add_audio(combined_video, AudioFileClip(voiceover))
    combined_video = burn_captions(
        combined_video, captions, fontsize=40, stroke_width=2)
    combined_video = change_video_speed(combined_video, 1.1)
    print(" Done!")

    final_video_path = write_video(combined_video, TEMP_DIR)

    # Send video
    if send_video_flag:
        print("Sending video...", end="")
        send_video(final_video_path)
        print(" Done!")


if __name__ == "__main__":
    article = get_article()

    generate_video(article, True)
