import requests
import json
from time import time

url = 'http://localhost:8000/'
theid = 'TESTING'
secret = 'TESTING_S'

cache = {}

def get_total_time_and_goal() -> tuple[int, int, int, bool]:
    if 1 not in cache.keys():
        req = requests.get(url+f'users/{theid}/statusbar/today?api_key={secret}', headers={'Authorization': f'Bearer {secret}'})
        data = json.loads(req.text)
        cache[1] = [int(time()+1800), ((int(data['data']['grand_total']['total_seconds'])), \
        (int(data['data']['goal']['target_seconds'])), \
        (int(data['data']['goal']['tracked_seconds'])))]

        return (int(data['data']['grand_total']['total_seconds'])), \
        (int(data['data']['goal']['target_seconds'])), \
        (int(data['data']['goal']['tracked_seconds'])), True
    else:
        if cache[1][0] >= time():
            return cache[1][1] + tuple([False])
        else:
            req = requests.get(url+f'users/{theid}/statusbar/today?api_key={secret}', headers={'Authorization': f'Bearer {secret}'})
            data = json.loads(req.text)
            cache[1] = [int(time()+1800), ((int(data['data']['grand_total']['total_seconds'])), \
            (int(data['data']['goal']['target_seconds'])), \
            (int(data['data']['goal']['tracked_seconds'])))]

            return (int(data['data']['grand_total']['total_seconds'])), \
            (int(data['data']['goal']['target_seconds'])), \
            (int(data['data']['goal']['tracked_seconds'])), True