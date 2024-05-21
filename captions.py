import os
import subprocess
import time
import uuid
import boto3
import requests
from srt_equalizer import srt_equalizer

CHARS_PER_LINE = 40

BUCKET = "martinngs-bucket"


def generate_captions_aws(audio_path: str, tmp_path: str):
    subprocess.run(["aws", "s3", "cp", audio_path,
                   f"s3://{BUCKET}/newsshorts/"])

    transcribe = boto3.client('transcribe')
    jobname = os.path.basename(audio_path)

    response = transcribe.start_transcription_job(
        TranscriptionJobName=jobname,
        LanguageCode='en-US',
        MediaFormat='mp3',
        Media={
            'MediaFileUri': "s3://martinngs-bucket/newsshorts/" + os.path.basename(audio_path)
        },
        Subtitles={
            'Formats': [
                'srt',
            ],
            'OutputStartIndex': 0
        },
    )

    while (response['TranscriptionJob']['TranscriptionJobStatus'] == 'IN_PROGRESS'):
        time.sleep(1)
        response = transcribe.get_transcription_job(
            TranscriptionJobName=jobname)

    result = requests.get(
        response['TranscriptionJob']['Subtitles']['SubtitleFileUris'][0])

    output_path = os.path.join(tmp_path, f"{uuid.uuid4()}.srt")

    with open(output_path, 'w') as file:
        # SRT files require two empty lines at the end
        file.write(result.text + "\n\n")

    srt_equalizer.equalize_srt_file(
        output_path, output_path, CHARS_PER_LINE, method='halving')

    subprocess.run(["aws", "s3", "rm",
                   f"s3://{BUCKET}/newsshorts/{os.path.basename(audio_path)}"])

    return output_path
