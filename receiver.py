import time
from datetime import datetime

import requests


def pretty_print(message):
    """
    2020/09/08 10:00:23  Nick
    Message

    """
    dt = datetime.fromtimestamp(message['timestamp'])
    dt = dt.strftime('%Y/%m/%d %H:%M')
    first_line = dt + '  ' + message['name']
    print(first_line)
    print(message['text'])
    print()


url = 'http://127.0.0.1:5000/messages'
after_id = -1

while True:
    response = requests.get(url, params={'after_id': after_id})
    messages = response.json()['messages']
    for message in messages:
        pretty_print(message)
        after_id = message['id']

    if not messages:
        time.sleep(1)
