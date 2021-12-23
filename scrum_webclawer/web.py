import requests
import json
from Event import Event
from apscheduler.schedulers.blocking import BlockingScheduler


def run():
    event = Event()

    url = "https://www.feishu.cn/flow/api/trigger-webhook/6bd6f07976f7adfdd3775827b67bfbe8"

    payload = {"events": [event.get_event()]}
    print(payload)
    payload = json.dumps(payload)

    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response)

run()
#
# schedule = BlockingScheduler()
# schedule.add_job(run, trigger="cron", hour=18, minute=00)
# schedule.start()