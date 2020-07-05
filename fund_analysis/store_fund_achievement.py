#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @File : store_fund_achievement.py
# @Desc : 

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import time
import json
import requests
import datetime
from fund.common import insert, selects
from fund.fund_analysis.store_all_fund import headers


def get_fund_scale(fund_code):
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jzcgm&code={fund_code}".format(fund_code=fund_code)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = r.text.split('var jzcgm_apidata=')[-1]
        if res:
            return json.loads(res)[-1][-1]
        return 0
    else:
        print("Get fund's scale from {url} is failed".format(url=url))
        return


def get_fund_increase_info(fund_code):
    tengxun_url = "http://web.ifzq.gtimg.cn"
    url_ = tengxun_url + "/fund/newfund/fundBase/getRankInfo"
    jjstring = 'jj' + str(fund_code)
    params = {'symbol': jjstring}
    r = requests.get(url_, params=params, headers=headers)
    print(r.status_code, r.text)
    if r.status_code == 200 and r.json()['code'] == 0:
        return r.json()['data']['jzzf']
    return {"w1": 0, "w4": 0, "w13": 0, "w26": 0, "w52": 0, "year": 0, "total": 0, "year3": 0}


def generat_sql_for_insert_fund_achievement(fund_code_list):
    times = 0
    today_date = datetime.date.today()
    sql = "INSERT INTO `fund`.`fund_achievement` (`date`, `code_id`, `scale`, `week1`, `month1`, `month3`, `month6`, `year1`, `year3`) VALUES "
    for code_id in fund_code_list:
        achievement_dic = get_fund_increase_info(code_id)
        tuples = (today_date, code_id, get_fund_scale(code_id), achievement_dic['w1'], achievement_dic['w4'], achievement_dic['w13'], achievement_dic['w26'], achievement_dic['year'], achievement_dic['year3'])
        sql = sql + str(tuples) + ','
        if times % 300 == 0:
            time.sleep(60)
    print(sql)
    return sql.strip(',')


def get_fund_code():
    code_lst = []
    res_lst = selects("select code_id from all_funds")
    for r in res_lst:
        code_lst.append(r['code_id'])
    return code_lst


if __name__ == '__main__':
    fund_code_list = get_fund_code()
    print(fund_code_list)
    generat_sql_for_insert_fund_achievement(fund_code_list)