import os
import uuid
import assemblyai as aai
import srt_equalizer
from dotenv import load_dotenv

load_dotenv("./.env")

ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")
CHARS_PER_LINE = 20


def generate_captions(audio_path: str, path: str) -> str:
    """
    Generates captions for an audio file.

    Args:
        audio_path (str): The path to the audio file.
        path (str): The path to save the captions to.

    Returns:
        str: The path to the generated captions.
    """

    subs_id = uuid.uuid4()
    subs_path = f"{path}/{subs_id}.srt"

    aai.settings.api_key = ASSEMBLY_AI_API_KEY
    transcript = aai.Transcriber().transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt()

    print(subtitles)

    with open(subs_path, 'w') as file:
        file.write(subtitles)

    srt_equalizer.equalize_srt_file(subs_path, subs_path, 20)

    return subs_path
