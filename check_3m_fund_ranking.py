#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : check_3m_fund_ranking.py
# @Date : 2020/3/11 
# @Desc :

import operator
import datetime
from common import send_mail
from index_for_fund_auto_notification import select_fund_seek_bank,change_fund_increase_dic

def get_result_fund_lst2(fund_data, sort_key='three_month'):
    result_lst = []
    for data_dic in fund_data:
        fund_increase_dic = change_fund_increase_dic(data_dic['code_id'], data_dic['name'])
        fund_increase_dic.pop('code_id')
        fund_increase_dic.pop('six_month')
        fund_increase_dic.pop('one_year')
        fund_increase_dic.pop('three_year')
        result_lst.append(fund_increase_dic)
    sorted_result_lst = sorted(result_lst, key=operator.itemgetter(sort_key), reverse=True)
    return sorted_result_lst

def get_mail_fund_content(mode='fund'):
    fund_data = select_fund_seek_bank(mode)
    print("fund_data===========" + str(fund_data))
    result_fund_bank_lst = get_result_fund_lst2(fund_data)
    print("result_fund_bank_lst===========" + str(result_fund_bank_lst))
    result_fund_bank_content = '\n'.join([' '.join([str(v) for v in x.values()]) for x in result_fund_bank_lst])
    return result_fund_bank_content

def main():
    print("Today's date: " + str(datetime.now()))
    # 股票基金
    result_fund_bank_content = get_mail_fund_content(mode='fund')
    # 债券基金
    result_stock_bank_content = get_mail_fund_content(mode='stock')
    desc = '''
                一周  一月  三月↓
    '''
    dividing_line = "-----------------债券基金-----------------"
    send_mail("基金种子季报", [desc, result_fund_bank_content, dividing_line, result_stock_bank_content])
    print(result_fund_bank_content)
    print(result_stock_bank_content)