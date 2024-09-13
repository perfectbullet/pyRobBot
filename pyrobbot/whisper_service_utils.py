import io

import requests
from loguru import logger

whisper_base_url = 'http://localhost:9000/asr'


def transcribe(wav_buffer):
    '''
    音频 io 转文本
    '''

    headers = {
        'accept': 'application/json',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    params = {
        'encode': 'true',
        'task': 'transcribe',
        'language': 'zh',
        'initial_prompt': '返回结果简体中文',
        'word_timestamps': 'false',
        'output': 'txt',
    }

    fname = wav_buffer.name
    files = {
        'audio_file': (fname, wav_buffer, 'audio/wav'),
    }
    response = requests.post(whisper_base_url, params=params, headers=headers, files=files)
    txt = response.content.decode('utf-8')
    logger.info('whisper result is {}'.format(txt))
    return txt


if __name__ == '__main__':
    file_path = '../tests/你不要让我做饭啦我什么都能办到但是真的不会做饭.wav'
    with open(file_path, 'rb') as f:
        byteio = io.BytesIO(f.read())
        byteio.name = 'ok'
        result = transcribe(byteio)
        print('result is {}'.format(result))
