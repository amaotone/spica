import json
import time
from contextlib import contextmanager

import requests


def send_line_notification(message, config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    line_token = config['line_token']  # 終わったら無効化する
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = "\n{}".format(message)
    payload = {'message': message}
    headers = {'Authorization': 'Bearer {}'.format(line_token)}  # 発行したトークン
    requests.post(line_notify_api, data=payload, headers=headers)


@contextmanager
def timer(name):
    t0 = time.time()
    print(f'[{name}] start')
    yield
    print(f'[{name}] done in {time.time() - t0:.0f} s')


def timestamp():
    return time.strftime('%y%m%d_%H%M%S')
