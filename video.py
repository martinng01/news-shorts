from typing import List
import uuid
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize


def resize_footage(video_path: str, directory: str) -> str:
    """
    Resizes a video to 1080x1920 and crops it to 1080x1920.

    Args:
        video_path (str): The path to the video.
        directory (str): The directory to save the resized video.

    Returns:
        str: The path to the resized video.
    """
    video_id = uuid.uuid4()
    output_path = f"{directory}/{video_id}.mp4"

    clip = VideoFileClip(video_path)
    clip = resize(clip, height=1920)
    clip = crop(clip, x_center=960, y_center=960, width=1080, height=1920)

    clip.audio = None

    clip.write_videofile(output_path, threads=4, codec="mpeg4")
    return output_path


def combine_footage(video_paths: List[str], max_duration: int, directory: str) -> str:
    """
    Combines multiple videos into one video.

    Args:
        video_paths (List[str]): A list of paths to the videos.
        max_duration (int): The maximum duration of the video in seconds.
        directory (str): The directory to save the combined video.

    Returns:
        str: The path to the combined video.
    """
    video_id = uuid.uuid4()
    output_path = f"{directory}/{video_id}.mp4"
    clip_duration = max_duration / len(video_paths)

    clips = [VideoFileClip(video_path).subclip(0, clip_duration)
             for video_path in video_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, threads=4, codec="mpeg4")

    return output_path


def add_audio(combined_video_path: str, tts_path: str, directory: str) -> str:
    """
    Adds audio to a video.

    Args:
        combined_video_path (str): The path to the combined video.
        tts_path (str): The path to the TTS audio.
        directory (str): The directory to save the final video.

    Returns:
        str: The path to the final video.
    """

    video_id = uuid.uuid4()
    output_path = f"{directory}/{video_id}.mp4"

    result: VideoFileClip = VideoFileClip(combined_video_path).set_audio(
        AudioFileClip(tts_path))

    result.write_videofile(output_path, threads=4, codec="mpeg4",
                           temp_audiofile=f"{directory}/temp-audio.mp3",)

    return output_path
