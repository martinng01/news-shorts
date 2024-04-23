from typing import List, Tuple, cast
import uuid
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.video.fx.speedx import speedx


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
    video.write_videofile(video_path, codec="libx264")

    return video_path


def change_video_speed(video: VideoFileClip | CompositeVideoClip, speed: float) -> VideoFileClip:
    """
    Changes the speed of the audio in a video.

    Args:
        video (VideoFileClip): The video to change the audio speed of.
        speed (float): The speed to change the audio to.

    Returns:
        VideoFileClip: The video with the audio speed changed.
    """
    return speedx(video, speed)


# def change_audio_speed(audio: AudioFileClip, speed: float, path: str) -> str:
#     audio_path = f"{path}/{uuid.uuid4()}.mp4"
#     audio.write_audiofile(audio_path, ffmpeg_params=[
#                           "-filter_complex", "\"[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]\"", "-map", "[v]", "-map", "[a]"])

#     return audio_path


# change_audio_speed(AudioFileClip(
#     'tmp/87c31cfc-9cc7-4f73-8ede-9fe1a2e3d72a.mp4'), 1.2, 'tmp')


def burn_captions(video: VideoFileClip, captions_path: str, fontsize: int, stroke_width: int) -> CompositeVideoClip:
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
            color='white',
            stroke_color="black",
            stroke_width=stroke_width,
        )

    subtitles = SubtitlesClip(captions_path, generator)
    result = CompositeVideoClip(
        [video, subtitles.set_position(('center', 'center'))])

    return result
