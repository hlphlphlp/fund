#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @File : store_all_fund.py
# @Desc : 
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import json
import requests
from fund.common import insert

headers = {"Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
           }


def get_all_funds():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = r.text.split('var r =')[-1].strip(';')
        return json.loads(res)
    else:
        print("Get funds from http://fund.eastmoney.com/js/fundcode_search.js is failed")
        return


def generat_sql_for_insert_all_funds():
    funds = get_all_funds()
    sql = "INSERT INTO `fund`.`all_funds` (`code_id`,	`name`,	`type`) VALUES "
    for fund in funds:
        tuples = (fund[0], fund[2], fund[3])
        sql = sql + str(tuples) + ','
    return sql.strip(',')


def store_funds():
    sql = generat_sql_for_insert_all_funds()
    insert(sql)


if __name__ == '__main__':
    store_funds()
