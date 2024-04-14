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

    # Get stock footage for each search term
    video_paths = []
    for search_term in search_terms:
        print(f"Getting footage for search term {search_term}...", end="")
        stock_footage = get_stock_footage(search_term, 1, 5)
        if stock_footage is None:
            print(" No footage found.")
            continue
        video_path = download_footage(stock_footage[0], TEMP_DIR)
        video_paths.append(video_path)
        print(" Done!")
        print(video_path)
        print()

    # Combine and resize footage
    print("Combining and resizing footage...", end="")
    combined_video = combine_footage(
        [resize_footage(video_path, TEMP_DIR) for video_path in video_paths], AudioFileClip(voiceover).duration, TEMP_DIR)
    print(" Done!")

    # Add audio to video
    print("Adding audio to video...", end="")
    final_video = add_audio(combined_video, voiceover, TEMP_DIR)
    print(" Done!")

    # Send video
    if send_video_flag:
        print("Sending video...", end="")
        send_video(final_video)
        print(" Done!")


if __name__ == "__main__":
    article = get_article()

    generate_video(article, False)
