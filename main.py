from footage import *
from gpt import *
from voice import *
from editor import *
from bot import *
from news import *
from captions import *

TEMP_DIR = "tmp"


def generate_video(article: str, img_paths: List[str], send_video_flag: bool = False):
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
    voiceover = tts(script, TEMP_DIR)
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

    # Send video
    if send_video_flag:
        print("Sending video...", end="")
        send_video(combined_video)
        print(" Done!")

    # Cleanup tmp files
    for path in temp_paths:
        os.remove(path)


if __name__ == "__main__":
    article, img_paths = get_cna_article(
        TEMP_DIR, target_url="")
    generate_video(article, img_paths, False)
