import uuid
import os
import boto3


def generate_audio_aws(text: str, tmp_path: str):
    output_path = os.path.join(tmp_path, f"{uuid.uuid4()}.mp3")

    polly = boto3.client("polly")

    try:
        response = polly.synthesize_speech(
            Engine="neural", OutputFormat="mp3", Text=text, VoiceId="Danielle"
        )
    except Exception as e:
        print(e)

    with open(output_path, "wb") as file:
        file.write(response["AudioStream"].read())

    return output_path
