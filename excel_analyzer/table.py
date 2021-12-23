import json
import pandas as pd
from datetime import datetime
from collections import defaultdict


class Table:
    def __init__(self, xlsx_name, time_sids):
        self.xlsx_name = xlsx_name
        self.time_sids = time_sids
        self.summary_tables = dict()
        self.child_tables = dict()
        self.list_of_biz_key = []
        self.list_of_model_data = []
        self.all_sheets = defaultdict(list)
        self.all_sheets["基本信息"] = []

    @staticmethod
    def trans(timestamp):
        if not timestamp:
            return False
        if isinstance(timestamp, str):
            timestamp = int(timestamp)
        date = datetime.fromtimestamp(timestamp // 1000)
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def data_clean(value):
        if isinstance(value, list):
            value = ' '.join(map(str, value))
        if isinstance(value, str):
            value = value.replace('"', '')
            value = value.replace('[', '').replace(']', '')
        return value

    @staticmethod
    def struct_to_dict(df):
        res = dict()
        sids = df.iloc[:, 0].values
        name = df.iloc[:, 1].values
        for i in range(len(sids)):
            res[sids[i]] = name[i]
        return res

    def time_sids_process(self, value):
        if not isinstance(value, list):
            value = [value]
        period = [self.trans(times) for times in value]
        if not any(period):
            return ''
        period = '至'.join(period)
        return period

    def process_child_table(self, child_struct, value, biz_key):
        rows, nil = [], False
        for item in value:
            row = {'biz_key': biz_key}
            for k in item:
                if 'value' not in k:
                    continue
                sid, value = k['id'], k['value']
                if sid not in child_struct:
                    continue
                if sid in self.time_sids:
                    value = self.time_sids_process(value)
                nil = nil or value
                row[child_struct[sid]] = self.data_clean(value)
            rows.append(row)
        return rows if nil else []

    def read_struct(self):
        sheet_names = pd.ExcelFile(self.xlsx_name).sheet_names

        for idx, sn in enumerate(sheet_names):
            df = pd.read_excel(self.xlsx_name, sheet_name=sn, header=None)
            if idx == 0:
                self.summary_tables = self.struct_to_dict(df)
                continue
            child_table_sid = df.iloc[0, :][0]
            child_table = self.struct_to_dict(df)
            self.child_tables[child_table_sid] = child_table

    def read_table(self):
        df = pd.read_csv('data1.csv', encoding="gbk")
        self.list_of_model_data = df['model_data'].values
        self.list_of_biz_key = df['biz_key'].values

    def process_summary_table(self, sid, value):
        if sid in self.time_sids:
            return self.time_sids_process(value)
        return self.data_clean(value)

    def parse_multiple_json(self):
        length = len(self.list_of_model_data)
        for i in range(length):
            curr_model_data = self.list_of_model_data[i]
            curr_biz_key = self.list_of_biz_key[i]
            self.parse_single_json(curr_biz_key, curr_model_data)

    def parse_single_json(self, biz_key, model_data):
        model_data_json = json.loads(model_data)
        res_of_summary = {'biz_key': biz_key}

        for k in model_data_json:
            sid, value = k['id'], k['value']
            if sid in self.summary_tables:
                name_of_sid = self.summary_tables[sid]
                summary_res = self.process_summary_table(sid, value)
                res_of_summary[name_of_sid] = summary_res

            if sid in self.child_tables:
                child_table_name = self.child_tables[sid][sid]
                child_table_name = child_table_name.replace(' ', '')

                child_res = self.process_child_table(self.child_tables[sid], value, biz_key)
                self.all_sheets[child_table_name] += child_res
        self.all_sheets["基本信息"].append(res_of_summary)

    def run(self):
        self.read_struct()
        self.read_table()
        self.parse_multiple_json()

        writer = pd.ExcelWriter('result.xlsx')
        for k, v in self.all_sheets.items():
            df = pd.DataFrame(v)
            df.to_excel(writer, sheet_name=k, index=False, engine='xlsxwriter')
        writer.save()


if __name__ == '__main__':
    tmp = {
        "cder8c2b3qyfki",
        "cne9m301g9nowz",
        "ctbz95siyia4mi",
        "cxvxdinhthbb9u",
        "cj5899y3z4st20"}

    table = Table(xlsx_name='struct3.xlsx', time_sids=tmp)
    table.run()
