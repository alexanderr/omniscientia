import json


def get_config():
    with open('config.json') as f:
        return json.load(f)


def get_commands():
    with open('sfx_commands.json') as f:
        return json.load(f)


def save_config(conf):
    with open('config.json', 'w') as c:
        json.dump(conf, c, indent=2, separators=(',', ': '))
