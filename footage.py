
import os
import uuid
from dotenv import load_dotenv
import requests
from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


load_dotenv("./.env")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def get_stock_footage(query: str, num_videos: int, min_dur: int) -> List[str]:
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
    response = r.json()

    raw_urls = []
    video_urls = []
    try:
        for i in range(num_videos):
            # check if video has desired minimum duration
            if response["videos"][i]["duration"] < min_dur:
                continue
            raw_urls = response["videos"][i]["video_files"]

            video_url = raw_urls[i]["link"]
            if (video_url.endswith(".mp4")):
                video_urls.append(video_url)
    except Exception as e:
        print("No Videos found.")
        print(e)

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


def combine_resize_footage(video_paths: List[str], max_duration: int, directory: str = "./tmp"):
    video_id = uuid.uuid4()
    combined_video_path = f"{directory}/{video_id}.mp4"

    clip_duration = max_duration / len(video_paths)

    clips = []
    for video_path in video_paths:
        clip = VideoFileClip(video_path)
        clip.audio = None
        clip = clip.subclip(0, clip_duration)

        if round((clip.w/clip.h), 4) < 0.5625:
            clip = crop(clip, width=clip.w, height=round(clip.w/0.5625),
                        x_center=clip.w / 2,
                        y_center=clip.h / 2)
        else:
            clip = crop(clip, width=round(0.5625*clip.h), height=clip.h,
                        x_center=clip.w / 2,
                        y_center=clip.h / 2)
        clip = resize(clip, height=1080, width=1920)

        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(combined_video_path, threads=4, codec="mpeg4")

    return combined_video_path


get_stock_footage("Middle East", 1, 5)
