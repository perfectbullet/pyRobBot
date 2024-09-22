import json


if __name__ == '__main__':
    fpath = "/tmp/tmpk_fqbssg/parsed_args_2174f39fa112434e9541f661258cf8c9.pkl"
    with open(fpath, "r") as configs_file:
        data = json.load(configs_file)
        data['context_model'] = 'full-history'
        # data['initial_greeting'] = '你好'
        print(data)
