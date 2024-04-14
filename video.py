import uuid
from moviepy.editor import VideoFileClip, AudioFileClip


def add_audio(combined_video_path: str, tts_path: str, directory: str) -> str:
    """
    This function creates the final video, with subtitles and audio.

    Args:
        combined_video_path (str): The path to the combined video.
        tts_path (str): The path to the text-to-speech audio.
        subtitles_path (str): The path to the subtitles.
        threads (int): The number of threads to use for the video processing.
        subtitles_position (str): The position of the subtitles.

    Returns:
        str: The path to the final video.
    """

    video_id = uuid.uuid4()
    video_path = f"{directory}/{video_id}.mp4"

    result: VideoFileClip = VideoFileClip(combined_video_path).set_audio(
        AudioFileClip(tts_path))

    result.write_videofile(video_path, threads=2, codec="mpeg4",
                           temp_audiofile=f"{directory}/temp-audio.mp3",)

    return video_path
