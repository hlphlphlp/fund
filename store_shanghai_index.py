#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : store_shanghai_index.py
# @Date : 2020/3/1 
# @Desc :

import requests
from common import headers, insert

def get_tengxun_info():
    tengxun_url = 'http://web.sqt.gtimg.cn'
    url_ = tengxun_url + "/q=sh000001"
    r = requests.get(url_, headers=headers)
    # print(r.status_code, r.text)
    if r.status_code == 200:
        return r.text
    return

def get_value_from_tengxun_info():
    index_info = get_tengxun_info()
    index_lst = index_info.split('~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~~')
    index_lst0 = index_lst[0].split("~")
    index_lst1 = index_lst[1].split("~")
    print("index_lst0: " + str(index_lst0))
    print("index_lst1: " + str(index_lst1))
    name = index_lst0[1]
    id = index_lst0[2]
    current_value = index_lst0[3]
    yesterday_end = index_lst0[4]
    today_begin = index_lst0[5]
    today_highest = index_lst1[3]
    today_lowest = index_lst1[4]
    deal_count = round(int(index_lst0[6])/100000000, 2)
    deal_money = round(int(index_lst1[7])/10000, 2)
    compare_to_yesterday = index_lst1[1]
    amplitude = index_lst1[2]

    return {'name': name, 'id': id, 'current_value': current_value, 'yesterday_end': yesterday_end, 'today_begin': today_begin,
            'today_highest': today_highest, 'today_lowest': today_lowest, 'deal_count': deal_count, 'compare_to_yesterday': compare_to_yesterday,
            'amplitude': amplitude, 'deal_money': deal_money}



def save_data(result_dic):
    sql = '''
    INSERT INTO shanghai_index (
        `code_id`,
        `name`,
        `current_value`,
        `yesterday_end`,
        `today_begin`,
        `today_highest`,
        `today_lowest`,
        `deal_count`,
        `compare_to_yesterday`,
        `amplitude`,
        `deal_money`
        )
    VALUES
        (
            '{code_id}',
            '{name}',
            '{current_value}',
            '{yesterday_end}',
            '{today_begin}',
            '{today_highest}',
            '{today_lowest}',
            '{deal_count}',
            '{compare_to_yesterday}',
            '{amplitude}',
            '{deal_money}'
        );
'''.format(name=result_dic['name'], code_id=result_dic['id'], current_value=result_dic['current_value'], yesterday_end=result_dic['yesterday_end'],
               today_begin=result_dic['today_begin'], today_highest=result_dic['today_highest'], today_lowest=result_dic['today_lowest'], amplitude=result_dic['amplitude'],
               deal_count=result_dic['deal_count'], deal_money=result_dic['deal_money'], compare_to_yesterday=result_dic['compare_to_yesterday'])
    print("==================save success!")
    print(sql)
    insert(sql)


if __name__ == '__main__':
    result_dic = get_value_from_tengxun_info()
    save_data(result_dic)