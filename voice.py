# credit: https://github.com/oscie57/tiktok-voice

from typing import List, Tuple
import uuid
from dotenv import load_dotenv
import requests
import base64
import os

VOICES = [
    # DISNEY VOICES
    "en_us_ghostface",  # Ghost Face
    "en_us_chewbacca",  # Chewbacca
    "en_us_c3po",  # C3PO
    "en_us_stitch",  # Stitch
    "en_us_stormtrooper",  # Stormtrooper
    "en_us_rocket",  # Rocket
    # ENGLISH VOICES
    "en_au_001",  # English AU - Female
    "en_au_002",  # English AU - Male
    "en_uk_001",  # English UK - Male 1
    "en_uk_003",  # English UK - Male 2
    "en_us_001",  # English US - Female (Int. 1)
    "en_us_002",  # English US - Female (Int. 2)
    "en_us_006",  # English US - Male 1
    "en_us_007",  # English US - Male 2
    "en_us_009",  # English US - Male 3
    "en_us_010",  # English US - Male 4
    # EUROPE VOICES
    "fr_001",  # French - Male 1
    "fr_002",  # French - Male 2
    "de_001",  # German - Female
    "de_002",  # German - Male
    "es_002",  # Spanish - Male
    # AMERICA VOICES
    "es_mx_002",  # Spanish MX - Male
    "br_001",  # Portuguese BR - Female 1
    "br_003",  # Portuguese BR - Female 2
    "br_004",  # Portuguese BR - Female 3
    "br_005",  # Portuguese BR - Male
    # ASIA VOICES
    "id_001",  # Indonesian - Female
    "jp_001",  # Japanese - Female 1
    "jp_003",  # Japanese - Female 2
    "jp_005",  # Japanese - Female 3
    "jp_006",  # Japanese - Male
    "kr_002",  # Korean - Male 1
    "kr_003",  # Korean - Female
    "kr_004",  # Korean - Male 2
    # SINGING VOICES
    "en_female_f08_salut_damour",  # Alto
    "en_male_m03_lobby",  # Tenor
    "en_female_f08_warmy_breeze",  # Warmy Breeze
    "en_male_m03_sunshine_soon",  # Sunshine Soon
    # OTHER
    "en_male_narration",  # narrator
    "en_male_funny",  # wacky
    "en_female_emotional",  # peaceful
]

load_dotenv("./.env")

API_BASE_URL = f"https://api16-normal-v6.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"
TIKTOK_SESSION_ID = os.getenv("TIKTOK_SESSION_ID")


def tts(text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech",
        directory: str = './tmp'):
    video_id = uuid.uuid4()
    video_path = f"{directory}/{video_id}.mp4"

    split_text = split_string(req_text, 250)

    b64d_arr = []
    for text in split_text:
        vstr, scode = generate_audio(text_speaker, text)
        if (scode != 0):
            print(f"Error generating text audio, Status Code: {scode}")

        b64d = base64.b64decode(vstr)

        b64d_arr.append(b64d)

    with open(video_path, "wb") as out:
        for b64d in b64d_arr:
            out.write(b64d)

    return video_path


def generate_audio(text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech",) -> Tuple[str, int]:
    """
    Generate audio from text using the TikTok Text to Speech API.

    Args:
        text_speaker (str): The voice to use.
        req_text (str): The text to convert to speech.

    Returns:
        Tuple[str, int]: The base64-encoded audio data and the status code.
    """
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")
    req_text = req_text.replace("ä", "ae")
    req_text = req_text.replace("ö", "oe")
    req_text = req_text.replace("ü", "ue")
    req_text = req_text.replace("ß", "ss")

    r = requests.post(
        f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233",
        headers={
            'User-Agent': USER_AGENT,
            'Cookie': f'sessionid={TIKTOK_SESSION_ID}'
        }
    )

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return ("", 5)

    vstr = [r.json()["data"]["v_str"]][0]
    scode = [r.json()["status_code"]][0]

    return (vstr, scode)


def split_string(string: str, n: int) -> List[str]:
    """
    Splits a string into multiple strings, each with a maximum length of n characters.

    Args:
        string (str): The string to split.
        n (int): The maximum length of each split string.

    Returns:
        List[str]: A list of strings, each with a maximum length of n characters.
    """

    words = string.split()
    result = []
    current_length = 0
    current_word = ""
    for word in words:
        if current_length + len(word) <= n:
            current_word += word + " "
            current_length += len(word) + 1
        else:
            result.append(current_word.strip())
            current_word = word + " "
            current_length = len(word) + 1
    if current_word:
        result.append(current_word.strip())
    return result


def sampler():
    """
    Generate a sample of the voices.
    """
    for item in VOICES:
        text_speaker = item
        filename = item
        print(item)
        req_text = 'Tiktok Text to Speech Test'
        tts(text_speaker, req_text, filename)
