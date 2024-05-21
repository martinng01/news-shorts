import math
import os
import subprocess
from typing import List, Tuple, cast
import uuid
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from PIL import Image
import numpy


def resize_footage(video, dimensions: Tuple[int, int]) -> VideoFileClip:
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

    res = crop(res, x_center=res.w / 2, y_center=res.h /
               2, width=target_width, height=target_height)

    return res


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


def add_audio(video_path: str, audio_path: str, tmp_path: str):
    """
    Adds audio to a video.

    Args:
        video (VideoFileClip): The video to add audio to.
        audio (AudioFileClip): The audio to add to the video.

    Returns:
        VideoFileClip: The video with the audio added.
    """

    output_path = os.path.join(tmp_path, f"{uuid.uuid4()}.mp4")

    subprocess.run(["ffmpeg", "-i", video_path, "-i", audio_path,
                   "-map", "0", "-map", "1:a", "-shortest", output_path])

    return output_path


def write_video(video, audio: str, path: str) -> str:
    """
    Writes a video to a file.

    Args:
        video (VideoFileClip): The video to write.
        path (str): The path to write the video to.

    Returns:
        str: The path to the written video.
    """
    video_path = os.path.join(path, f"{uuid.uuid4()}.mp4")
    video.write_videofile(video_path, audio=audio, codec="libx264")

    return video_path


def burn_captions(video: VideoFileClip, captions_path: str, fontsize: int, stroke_width: float) -> CompositeVideoClip:
    """
    Burns captions into a video.

    Args:
        video (VideoFileClip): The video to burn captions into.
        captions_path (str): The captions to burn into the video.

    Returns:
        VideoFileClip: The video with the captions burned in.
    """

    def generator(txt) -> TextClip:
        return TextClip(
            txt,
            font="fonts/bold_font.ttf",
            fontsize=fontsize,
            kerning=1,
            color='white',
            stroke_color="black",
            stroke_width=stroke_width,  # type: ignore
            method='caption',
            size=(300, 200)
        )

    subtitles = SubtitlesClip(captions_path, generator)
    result = CompositeVideoClip(
        [video, subtitles.set_position(('center', 'center'))])

    return result


def image_to_video(image_path: str, duration: int):
    """
    Converts an image to a video.

    Args:
        image_path (str): The path to the image.
        duration (int): The duration of the video.

    Returns:
        VideoFileClip: The video created from the image.
    """
    image = ImageClip(image_path, duration=duration)
    return zoom_in_effect(image, 0.02)


# https://gist.github.com/mowshon/2a0664fab0ae799734594a5e91e518d5
def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)  # type: ignore

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)  # type: ignore

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)
