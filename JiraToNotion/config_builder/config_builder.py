import json


def get_file_data(config_file):
    with open(config_file) as config:
        data = json.load(config)

    return data
