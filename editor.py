from typing import List, Tuple, cast
import uuid
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize


def resize_footage(video: VideoFileClip, dimensions: Tuple[int, int]) -> VideoFileClip:
    """
    Resizes a video to the specified dimensions.

    Args:
        video (VideoFileClip): The video to resize.
        dimensions (Tuple[int, int]): The dimensions to resize the video to.

    Returns:
        VideoFileClip: The resized video.
    """
    target_width, target_height = dimensions
    clip_width, clip_height = video.size

    if clip_width < clip_height:
        res = resize(video, width=target_width)
    else:
        res = resize(video, height=target_height)

    # FIXME
    res = crop(res, x_center=res.w / 2, y_center=res.h /
               2, width=target_width, height=target_height)

    return res


resize_footage(VideoFileClip(
    'tmp/243e7810-d7ba-4f5f-848e-ebbb818e058b.mp4'), (1080, 1920))


def combine_footage(videos: List[VideoFileClip], max_duration: int) -> VideoFileClip:
    """
    Combines multiple videos into a single video.

    Args:
        videos (List[VideoFileClip]): The videos to combine.
        max_duration (int): The maximum duration of the combined video.

    Returns:
        VideoFileClip: The combined video.
    """
    video_duration = max_duration / len(videos)
    trimmed_videos = [video.subclip(0, video_duration) for video in videos]

    return cast(VideoFileClip, concatenate_videoclips(trimmed_videos, method="compose"))


def add_audio(video: VideoFileClip, audio: AudioFileClip) -> VideoFileClip:
    """
    Adds audio to a video.

    Args:
        video (VideoFileClip): The video to add audio to.
        audio (AudioFileClip): The audio to add to the video.

    Returns:
        VideoFileClip: The video with the audio added.
    """

    return video.set_audio(audio)


def write_video(video: VideoFileClip, path: str) -> str:
    """
    Writes a video to a file.

    Args:
        video (VideoFileClip): The video to write.
        path (str): The path to write the video to.

    Returns:
        str: The path to the written video.
    """
    video_id = uuid.uuid4()
    video_path = f"{path}/{video_id}.mp4"
    video.write_videofile(video_path, codec="mpeg4", threads=4)

    return video_path

# TODO Implement this function


def change_audio_speed():
    pass
