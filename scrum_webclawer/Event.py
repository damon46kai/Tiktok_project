import requests
import json
import time

class Event:
    def __init__(self):
        self.headers = {
            'authority': 'approval.bytedance.com',
            'accept': 'application/json, text/plain, */*',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'post-id': '1j1h8b3hsxk81',
            'origin': 'https://approval.bytedance.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://approval.bytedance.com/wfc_agile/manage/dataManage?fb_key=ae0f610bcc9f4fedb468784aab2366a4',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'gftoken=NDI3MjA0ODE0MHwxNjAxOTY2NzUzMTZ8fDAGBgYGBgY; portal_token=09db0b23-54b1-4852-8163-ce235cd5ff1a; login_agent_type=lark; local=zh-CN; timezone=%28GMT%2B8%3A00%29%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4%26-%26%E4%B8%8A%E6%B5%B7%7C%28GMT%2B8%3A00%29China%26Standard%26Time%26-%26Shanghai%7C%28GMT%2B8%3A00%29%E4%B8%AD%E5%9B%BD%E6%A8%99%E6%BA%96%E6%99%82%26-%26%E4%B8%8A%E6%B5%B7%7C480%7CAsia%2FShanghai; agile_token=03341909-2502-4322-bf72-665dabe20764; MONITOR_WEB_ID=607ed1c5-9cb7-4619-b335-a586dad0a35d'

        }
        self.payload = {"page": {"page_index": 1, "page_size": 1000},
                        "orders": [{"column_name": "create_time", "desc": True}],
                        "query": {"biz_key": "", "creator": "", "approve_status": [], "start_time": None,
                                  "end_time": None}}
        self.url = "https://approval.bytedance.com/wfc_agile/api/v1/private/formData/ae0f610bcc9f4fedb468784aab2366a4/formDataList?ea_traceid=17561ba8-243f-45ce-a2bf-e4731c9bc8c8"



    def get_event(self):
        payload = json.dumps(self.payload)
        session = requests.Session()
        session.post(self.url, headers=self.headers, data=payload)

        response = session.post(self.url, headers=self.headers, data=payload)
        rsp = response.json()
        rows = rsp['data']['form_data_content']['rows']

        create_n = 0
        process_n = 0
        finish_n = 0
        count=0
        resource_response_num = 0
        bid_partner_num = 0
        bid_ongoing_num = 0
        resource_allocate_num = 0
        program_confirm_num = 0
        for item in rows:
            tmp = item['create_time']   #任务创建时间
            #if tmp > time.strftime("%Y-%m-%d"):
            if tmp >= "2020-11-03":
                create_n += 1
                #print(item['czs11hb2m3v5yz'], item['cnaytdvop628ti']) #项目编号; 数据量
                   # print(item['cnaytdvop628ti']) #数据量
                   # print(item['cyy5iktqau6avg']) #标注采集单价
            # if tmp >= "2020-11-03":
            #     print(item['biz_key'])
                #统计今天开始的任务数量
        print(time.strftime("%Y-%m-%d"))
        for item in rows:
            tmp = item['finish_time'] #任务完成时间

            if tmp is not '' and tmp > time.strftime("%Y-%m-%d") and item['process_status_type'] != "TERMINATED":
            #如果完成时间不为空，审批没有终止，统计当日通过的数量

                finish_n += 1
            elif item['process_status_type'] == "RUNNING":
            #统计正在响应的任务数量
                process_n += 1

        # print(time.strftime("%Y.%m.%d"), create_n, process_n, finish_n


        Str = {"time": time.strftime("%Y.%m.%d"), "start": create_n, "process": process_n, "finish": finish_n}
        return Str


if __name__ == '__main__':
    test = Event()
    r = test.get_event()
    print(r)
