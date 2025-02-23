# This Python file uses the following encoding: utf-8

import json
import subprocess
import time
from typing import Iterator

import requests

group_id = '1881319919820214446'    #your_group_id
api_key = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJhc2FjIGNob2kiLCJVc2VyTmFtZSI6ImFzYWMgY2hvaSIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODgxMzE5OTE5ODI4NjAzMDU0IiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTg4MTMxOTkxOTgyMDIxNDQ0NiIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6ImFzYS5jaG9pQGZ3ZC5jb20iLCJDcmVhdGVUaW1lIjoiMjAyNS0wMi0yMyAwMTo0MDowNiIsIlRva2VuVHlwZSI6MSwiaXNzIjoibWluaW1heCJ9.yuV-O10NkJfVCySsAwmtUwCkGRzRHNxDDcWgHCrAhvCdSH2rutevA2JZWucTldExsAP1EU9i--252r8EeMhtWzadvSIMhDCJysyfnzyjlYUeLdfqKSuOEF2IQEyncZD1cNBZDaGONQNq2VYZqlNuHedoJ1MKsjHJjSu3Dub_7CZuvix7KiXHsyzpgL5XydEqatTonGeauF5gI3__EfZNvxSSfUYyDTwv2mCwfKqi-6Kn2nboOurYch87h47bv_Q0Pwoi4iEy6PdNd0GU2a9ehVs2Gv8exC8zsQc-rPxdgUIZCnP_L_olLa7TLwfMz4vtzMByam7rOlq_0RtjWpWaZQ'    #your_api_key

file_format = 'mp3'  # support mp3/pcm/flac

url = "https://api.minimaxi.chat/v1/t2a_v2?GroupId=" + group_id
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}


def build_tts_stream_headers() -> dict:
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'authorization': "Bearer " + api_key,
    }
    return headers


def build_tts_stream_body(text: str) -> dict:
    body = json.dumps({
        "model": "speech-01-hd",
        "text": "深港馬拉松測試賽將於今日(23日)早上舉行",
        "stream": True,
        "language_boost":"cantonese",
        "voice_setting": {
            "voice_id": "Cantonese_CuteGirl",
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        }
    })
    return body





def call_tts_stream(text: str) -> Iterator[bytes]:
    tts_url = url
    tts_headers = build_tts_stream_headers()
    tts_body = build_tts_stream_body(text)

    response = requests.request("POST", tts_url, stream=True, headers=tts_headers, data=tts_body)
    for chunk in (response.raw):
        if chunk:
            if chunk[:5] == b'data:':
                data = json.loads(chunk[5:])
                if "data" in data and "extra_info" not in data:
                    if "audio" in data["data"]:
                        audio = data["data"]['audio']
                        yield audio




audio_chunk_iterator = call_tts_stream('')
#audio = audio_play(audio_chunk_iterator)

for a in audio_chunk_iterator:
    b=bytes.fromhex(a)
 
    with open('output.mp3', 'ab') as f:
        f.write(b)  