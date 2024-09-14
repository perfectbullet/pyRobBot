import requests
import json
import io

from loguru import logger
from pydub import AudioSegment

emotivoice_url = "http://127.0.0.1:9875/v1/audio/speech"


def tts_request(text: str, speaker_id: int, url: str, prompt=''):
    logger.info('tts text is {}'.format(text))
    payload = json.dumps({
        "input": text,
        "voice": str(speaker_id),
        "prompt": prompt,
        "language": "zh_us",
        "model": "emoti-voice",
        "response_format": "mp3",
        "speed": 1
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    logger.info('response of tts is {}'.format(response.status_code))
    # audio_path = '{}_{}_{}.mp3'.format(text, speaker_id, prompt)
    # with open(audio_path, mode='wb') as f:
    #     f.write(response.content)
    return response


if __name__ == '__main__':
    txt = "纳兰小姐，看在纳兰老爷子的面上，萧炎奉劝你几句话。三十年河东，三十年河西，莫欺少年穷！"

    response = tts_request(txt, 1018, emotivoice_url, prompt='开心')

    wav_buffer = io.BytesIO(response.content)
    # for mp3_stream_chunk in response.iter_content(chunk_size=4096):
    #     mp3_buffer.write(mp3_stream_chunk)
    # mp3_buffer.seek(0)

    audio = AudioSegment.from_mp3(wav_buffer)
    print('audio is {}'.format(audio))
