import json
import time
import datetime
import requests
from get_weekContent import GetTableContent
from apscheduler.schedulers.blocking import BlockingScheduler

count_machine = {"resource_response_num": 0,  #今日已响应量
                 "bid_partner_num": 0, #今日合作商配置中
                 "bid_ongoing_num": 0,  #今日试标进行中
                 "resource_allocate_num": 0, #今日-资源配置中
                 "program_confirm_num": 0, #
                 "create_n": 0,  #本周提交总量
                 "finish_n": 0  #本周配置完成总量
                 }


def process():
    now = datetime.datetime.now()
    monday = (now - datetime.timedelta(days=now.weekday()))
    biz_params = {
        "form_code": "ae0f610bcc9f4fedb468784aab2366a4",
        "start_date": time.strftime("%Y-%m-%d"),
        "end_date": time.strftime("%Y-%m-%d")}

    mon_params = {
        "form_code": "ae0f610bcc9f4fedb468784aab2366a4",
        "start_date": monday.strftime("%Y-%m-%d"),
        "end_date": time.strftime("%Y-%m-%d")}

    biz_params = json.dumps(biz_params)
    mon_params = json.dumps(mon_params)

    msg_id = "world"
    app_id = "cli_9f1cc7f544f6500c"
    secret = "85aae6f1-2fb8-11eb-bd92-df3459788b11"

    weektest = GetTableContent(app_id=app_id, secret=secret, biz_params=mon_params, msg_id=msg_id)
    weekresponse = weektest.run()

    for item in weekresponse['data']:
        tmp = item['current_node_name']
        count_machine['create_n'] += 1
        if tmp == "资源配置" or tmp == "资源配置,资源配置" or "配置方案审批-项目测" in tmp or "配置方案审批-资源测" in tmp or "资源配置方案审批-项目" in tmp or "资源配置方案审批-资源" in tmp or "资源使用确认" in tmp or \
                item['process_status'] == "APPROVED":
            count_machine['finish_n'] += 1

    test = GetTableContent(app_id=app_id, secret=secret, biz_params=biz_params, msg_id=msg_id)

    response = test.run()
    # print(response['data'][0])
    for item in response['data']:

        tmp = item['current_node_name']
        if item['process_status']:
            count_machine["resource_response_num"] += 1
        if "试标合作商配置" in tmp or "BPO方式" in tmp:
            count_machine["bid_partner_num"] += 1
        if "试标资源确认" in tmp or "试标结论同步" in tmp or "试标效果确认" in tmp :
            count_machine["bid_ongoing_num"] += 1
        if tmp == "资源配置" or tmp == "资源配置,资源配置":
            count_machine["resource_allocate_num"] += 1

    res = {"time": time.strftime("%Y.%m.%d"), "start": len(response['data'])}
    res.update(count_machine)
    return res

process_res = process()

def send1():
    url = "" #deleted

    payload = {"events": [process_res]}
    payload = json.dumps(payload)
    # print(payload)
    headers = {'Content-Type': 'application/json'}
    requests.request("POST", url, headers=headers, data=payload)



def send2():
    url = "" //deleted

    payload = {"events": [process_res]}
    payload = json.dumps(payload)
    # print(payload)
    headers = {'Content-Type': 'application/json'}
    requests.request("POST", url, headers=headers, data=payload)


send1()
send2()
# schedule = BlockingScheduler()
# schedule.add_job(send, trigger="cron", hour=9, minute=55)
# schedule.start()
