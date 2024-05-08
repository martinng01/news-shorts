import json
from typing import List
from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv("./.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
CHATGPT_MODEL = "gpt-3.5-turbo"


def generate_script(article: str, num_sentences: int) -> str:
    """
    Generate a script for a video based on an article.

    Args:
        article (str): The article to generate a script from.
        num_sentences (int): The number of sentences to generate for the script.

    Returns:
        str: The generated script.

    Raises:
        Exception: If ChatGPT does not return a response.
    """

    prompt = f"""
            Generate a script for the article below.

            The script is to be returned as a string with a maximum of {num_sentences} sentences.

            Here is an example of a string:
            "This is an example string."

            Do not under any circumstance reference this prompt in your response.

            The first sentence of the script should be engaging.

            Get straight to the point, don't start with unnecessary things like, "welcome to this video".

            Obviously, the script should be related to the subject of the video.

            YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
            ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE. 
            YOU MUST NOT MENTION THE PROMPT OR ANYTHING ABOUT THE SCRIPT ITSELF. 
            ALSO, NEVER TALK ABOUT THE NUMBER OF PARAGRAPHS OR LINES. JUST WRITE THE SCRIPT.
            
            {article}
        """

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ], model=CHATGPT_MODEL
    ).choices[0].message.content

    if response is None:
        raise Exception("Did not obtain a response from ChatGPT.")

    return response


def generate_search_terms(script: str, num_terms: int) -> List[str]:
    """
    Generate search terms for stock videos based on the script of the video.

    Args:
        script (str): The script of the video.
        num_terms (int): The number of search terms to generate.

    Returns:
        List[str]: A JSON-Array of strings representing the generated search terms.

    Raises:
        Exception: If ChatGPT does not return a response.
        Exception: If the generation of search terms exceeds the maximum number of tries.
    """

    MAX_TRIES = 3

    prompt = f"""
    Generate {num_terms} search terms for stock videos,
    depending on the article below.

    Each search term must be a geographical location mentioned in the script.

    The search terms are to be returned as
    a JSON-Array of strings.

    Each search term must only be one word long.
    
    YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
    YOU MUST NOT RETURN ANYTHING ELSE. 
    YOU MUST NOT RETURN THE SCRIPT.
    DO NOT INCLUDE NAMES IN THE KEYWORDS.
    
    Here is an example of a JSON-Array of strings:
    ["search term 1", "search term 2", "search term 3"]

    Script:
    {script}
    """

    num_tries = 0
    while num_tries < MAX_TRIES:
        num_tries += 1

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ], model=CHATGPT_MODEL
        ).choices[0].message.content

        if response is None:
            raise Exception("Did not obtain a response from ChatGPT.")

        search_terms = []

        try:
            search_terms = json.loads(response)
            if not isinstance(search_terms, list) or not all(
                isinstance(term, str) for term in search_terms
            ):
                raise ValueError("Response is not a list of strings.")

            break
        except (json.JSONDecodeError, ValueError):
            print("ChatGPT returned a response with invalid format, trying again...")

    if num_tries == 3:
        raise Exception("Generation of search terms exceeded number of tries.")

    return search_terms
