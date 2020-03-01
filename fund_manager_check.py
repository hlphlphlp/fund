#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : demo.py
# @Date : 2020/2/18
# @Desc :

import requests
from datetime import datetime
from common import headers, send_mail, selects

def get_fund_info(fund_code):
    tengxun_url = "http://qt.gtimg.cn/"
    url_ = tengxun_url + "q=s_jj{fund_code}".format(fund_code=fund_code)
    r = requests.get(url_, headers=headers)
    # print(r.status_code, r.text)
    if r.status_code == 200:
        return r.text
    return

def select_managers():
    sql = "select f.code_id,f.name as name,m.name as manager_name from fund_info f,fund_manager m where f.manager_id=m.id and f.useful='1';"
    return selects(sql)

def judge_manager_has_changed():
    manager_has_changed_lst = []
    code_managers_data = select_managers()
    for cm in code_managers_data:
        fund_info = get_fund_info(cm['code_id'])
        if cm['manager_name'] not in fund_info:
            manager_has_changed_lst.append([cm['code_id'], cm['name'], cm['manager_name']])
    return manager_has_changed_lst

def send_email_notice(manager_has_changed_lst):
    if manager_has_changed_lst:
        content = '\n'.join([' '.join([str(y) for y in x]) for x in manager_has_changed_lst])
        # print(content)
        subject = '你关注的基金的经理有变动！请务必考虑是否继续持有！'
        send_mail(subject, content)
        print(subject, " , send email success!")

def main():
    print("Today's date: " + str(datetime.now()))
    manager_has_changed_lst = judge_manager_has_changed()
    send_email_notice(manager_has_changed_lst)
    print(manager_has_changed_lst)

if __name__ == '__main__':
    main()