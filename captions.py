import os
import uuid
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv("./.env")

ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")
CHARS_PER_LINE = 30


def generate_captions(audio_path: str, tmp_path: str) -> str:
    """
    Generates captions for an audio file.

    Args:
        audio_path (str): The path to the audio file.
        path (str): The path to save the captions to.

    Returns:
        str: The path to the generated captions.
    """
    subs_path = os.path.join(tmp_path, f"{uuid.uuid4()}.srt")

    aai.settings.api_key = ASSEMBLY_AI_API_KEY

    transcript = aai.Transcriber().transcribe(data=audio_path)
    subtitles = transcript.export_subtitles_srt(chars_per_caption=40)

    with open(subs_path, 'w') as file:
        file.write(subtitles)

    return subs_path
