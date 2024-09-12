import os
import requests

whisper_base_url = 'http://localhost:9000/asr'


def transcribe(file_path):
    '''

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
    fname = os.path.basename(file_path)
    files = {
        'audio_file': (fname, open(file_path, 'rb'), 'audio/wav'),
    }
    response = requests.post(whisper_base_url, params=params, headers=headers, files=files)
    return response.content.decode('utf-8')


if __name__ == '__main__':
    file_path = '../tests/你不要让我做饭啦。我什么都能办到，但是真的不会做饭。.wav'
    result = transcribe(file_path)
    print('result is {}'.format(result))
