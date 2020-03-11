#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : fund_assessment.py
# @Date : 2020/3/11 
# @Desc :

import json
import re
import requests
from common import headers

def get_fund_content(code_id):
    url = "http://fundgz.1234567.com.cn/js/%s.js" % str(code_id)
    r = requests.get(url, headers=headers)
    if str(code_id) in r.text:
        return r.text
    else:
        print("get_fund_content request error!")

def get_fund_assessment(code_id):
    content = get_fund_content(code_id)
    assessment = re.findall(r'{\".+\"}', content)
    print(assessment)
    fund_json = json.loads(assessment[0])
    return fund_json['gszzl']

if __name__ == '__main__':
    content = get_fund_assessment(161005)
    print(content)

