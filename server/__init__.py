import os
import json

config_path = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/config.json'
api_key_path = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/api_key.json'

def config_to_environ() -> None:

    '''Creates the config variables and turns them into environment variables'''

    with open(config_path, 'r') as config:
        for key, value in json.load(config).items():
            os.environ[key] = value

    with open(api_key_path, 'r') as api_key:
        for key, value in json.load(api_key).items():
            os.environ[key] = value

config_to_environ()

import website
website.app.run()
