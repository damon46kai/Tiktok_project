import json
import requests
import hashlib
import datetime
import time

class GetTableContent:
    def __init__(self, app_id, secret, biz_params, msg_id):
        self.url = "https://approval.bytedance.com/wfc_agile/api/v1/open/form/getFormDetailByFormCode"  #根据表单Code获取表单详情
        #self.url = "https://approval.bytedance.com/wfc_agile/api/v1/open/process/getTaskProcessInfo"  # 获取流程审批记录
        self.app_id = app_id
        self.secret = secret
        self.biz_params = biz_params
        self.msg_id = msg_id

    @staticmethod
    def get_timestamp():
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        return timestamp

    @staticmethod
    def md5(string):
        m = hashlib.md5()
        m.update(string.encode("utf-8"))
        return m.hexdigest()

    def get_sign(self):
        timestamp = self.get_timestamp()
        sign = self.md5(self.secret + timestamp + self.biz_params + self.msg_id)
        return sign, timestamp

    def get_payload(self):
        sign, timestamp = self.get_sign()
        payload = {
            "app_id": self.app_id,
            "sign": sign,
            "timestamp": timestamp,
            "biz_params": self.biz_params,
            "msg_id": self.msg_id
        }
        return payload


    def run(self):
        payload = self.get_payload()
        payload = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", self.url, headers=headers, data=payload).json()
        return response


if __name__ == '__main__':
    now = datetime.datetime.now()
    monday = (now - datetime.timedelta(days=now.weekday()))
    x = {
        "form_code": "ae0f610bcc9f4fedb468784aab2366a4",
        "start_date": monday.strftime("%Y-%m-%d"),
        "end_date": time.strftime("%Y-%m-%d")}

    x = json.dumps(x)

    msg_id = "world"
    app_id = "cli_9f1cc7f544f6500c"
    secret = "" #deleted
    t = GetTableContent(app_id, secret, x, msg_id)
    print(t.run())
