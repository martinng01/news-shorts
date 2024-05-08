
import os
import uuid
from dotenv import load_dotenv
import requests
from typing import List

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
load_dotenv("./.env")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def get_stock_footage(query: str, num_videos: int, min_dur: int) -> List[str] | None:
    """
    Searches for stock videos based on a query.

    Args:
        query (str): The query to search for.
        num_videos (int): The number of videos to return.
        min_dur (int): The minimum duration of the video in seconds.

    Returns:
        List[str]: A list of stock videos.
    """

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    qurl = f"https://api.pexels.com/videos/search?query={query}"
    r = requests.get(qurl, headers=headers)

    try:
        response = r.json()

        raw_urls = []
        video_urls = []
        for i in range(num_videos):
            # Check if video has desired minimum duration
            if response["videos"][i]["duration"] < min_dur:
                continue
            raw_urls = response["videos"][i]["video_files"]

            video_url = raw_urls[i]["link"]
            if (video_url.endswith(".mp4")):
                video_urls.append(video_url)
    except Exception as e:
        print("No Videos found.")
        print(e)
        return None

    return video_urls


def download_footage(video_url: str, directory: str = "./tmp") -> str:
    """
    Saves a video from a given URL and returns the path to the video.

    Args:
        video_url (str): The URL of the video to save.
        directory (str): The path of the temporary directory to save the video to

    Returns:
        str: The path to the saved video.
    """
    video_id = uuid.uuid4()
    video_path = f"{directory}/{video_id}.mp4"
    with open(video_path, "wb") as f:
        f.write(requests.get(video_url).content)

    return video_path
