#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : save_five_star_fund.py
# @Date : 2020/2/29 
# @Desc :

from selenium import webdriver
import operator
from index_for_fund_auto_notification import change_fund_increase_dic
from common import insert
from time import sleep

url = "http://cn.morningstar.com/quickrank/default.aspx"
dr = webdriver.Chrome()
dr.get(url)
dr.maximize_window()

def search_stock_fund():
    # 纯债基金
    dr.find_element_by_id("ctl00_cphMain_cblCategory_13").click()
    # 普通债券
    dr.find_element_by_id("ctl00_cphMain_cblCategory_12").click()
    # 激进债券
    # dr.find_element_by_id("ctl00_cphMain_cblCategory_11").click()
    dr.find_element_by_id("ctl00_cphMain_btnGo").click()

def search_fund():
    dr.find_element_by_id("ctl00_cphMain_cblCategory_0").click()
    dr.find_element_by_id("ctl00_cphMain_cblCategory_5").click()
    dr.find_element_by_id("ctl00_cphMain_cblCategory_6").click()
    dr.find_element_by_id("ctl00_cphMain_btnGo").click()
    dr.find_element_by_partial_link_text("五年").click()

def get_five_star_fund(count=30):
    result_funds = []
    for page in range(20):
        funds_tree = dr.find_elements_by_css_selector('#ctl00_cphMain_gridResult tr[class^="grid"]')
        for fund_tree in funds_tree:
            fund_obj = fund_tree.find_elements_by_class_name("msDataText")
            fund_data = [data.text for data in fund_obj]
            print("fund_data: " + str(fund_data))
            if (len(result_funds)) < count:
                result_funds.append(fund_data)
            else:
                return result_funds
        # 翻页
        sleep(3)
        dr.find_element_by_id("ctl00_cphMain_AspNetPager1").find_element_by_link_text(">").click()

def save_data(code_id, name, type, useful=0):
    sql = "INSERT INTO stock_info (`code_id`, `name`, `type`, `useful`) VALUES ({code_id}, {name}, {type}, {useful});".format(code_id=code_id, name=name, type=type, useful=useful)
    print(sql)
    insert(sql)

def get_fund_name(funds_data, code_id):
    for fund in funds_data:
        if code_id in fund:
            return fund[1]

def smart_sorting(funds_lst, mode='ranking'):
    score_dic = {}
    sort_by_1_week = sorted(funds_lst, key=operator.itemgetter('one_week'))
    for i in range(len(sort_by_1_week)):
        if mode == 'ranking':
            score_dic[sort_by_1_week[i]['code_id']] = [i*0.1]
        elif mode == 'rise':
            score_dic[sort_by_1_week[i]['code_id']] = [sort_by_1_week[i]['one_week']]

    sort_by_1_month = sorted(funds_lst, key=operator.itemgetter('one_month'))
    for i in range(len(sort_by_1_month)):
        if mode == 'ranking':
            score_dic[sort_by_1_month[i]['code_id']].append(i*0.2)
        elif mode == 'rise':
            score_dic[sort_by_1_month[i]['code_id']].append(sort_by_1_month[i]['one_month'])

    sort_by_3_month = sorted(funds_lst, key=operator.itemgetter('three_month'))
    for i in range(len(sort_by_3_month)):
        if mode == 'ranking':
            score_dic[sort_by_3_month[i]['code_id']].append(i*0.3)
        elif mode == 'rise':
            score_dic[sort_by_3_month[i]['code_id']].append(sort_by_3_month[i]['three_month'])

    sort_by_6_month = sorted(funds_lst, key=operator.itemgetter('six_month'))
    for i in range(len(sort_by_6_month)):
        if mode == 'ranking':
            score_dic[sort_by_6_month[i]['code_id']].append(i*0.4)
        elif mode == 'rise':
            score_dic[sort_by_6_month[i]['code_id']].append(sort_by_6_month[i]['six_month'])

    sort_by_1_year = sorted(funds_lst, key=operator.itemgetter('one_year'))
    for i in range(len(sort_by_1_year)):
        if mode == 'ranking':
            score_dic[sort_by_1_year[i]['code_id']].append(i*1.1)
        elif mode == 'rise':
            score_dic[sort_by_1_year[i]['code_id']].append(sort_by_1_year[i]['one_year'])

    sort_by_3_year = sorted(funds_lst, key=operator.itemgetter('three_year'))
    for i in range(len(sort_by_3_year)):
        if mode == 'ranking':
            score_dic[sort_by_3_year[i]['code_id']].append(i*1.2)
        elif mode == 'rise':
            score_dic[sort_by_3_year[i]['code_id']].append(sort_by_3_year[i]['three_year'])

    print("score_dic=======================" + str(score_dic))

    score_result_list = sorted(score_dic.items(), key=lambda x: sum(x[1]), reverse=True)

    print("score_result_list=======================" + str(score_result_list))
    return score_result_list

def sorting_funds():
    search_fund()
    result_funds = get_five_star_fund(92)

    # 变成列表，里装字典
    result_funds_lst = []
    for fund in result_funds:
        # save_data(code_id=fund[0], name=fund[1], type=fund[2])
        result_funds_lst.append(change_fund_increase_dic(fund[0], fund[1]))
    # 自定义排序
    # sorted(result_funds_lst, key=operator.itemgetter('one_year'))
    # print('\n'.join([' '.join([str(v) for v in x.values()]) for x in result_funds_lst]))
    # smart排序
    smart_lst = []
    score_result_list = smart_sorting(result_funds_lst, mode='ranking')
    for i in range(len(score_result_list)):
        code_id = score_result_list[i][0]
        smart_lst.append(change_fund_increase_dic(code_id, get_fund_name(result_funds, code_id)))
    print('\t'.join([str(v) for v in result_funds_lst[0].keys()]))
    print('\n'.join(['\t'.join([str(v) for v in x.values()]) for x in smart_lst]))



if __name__ == '__main__':
    sorting_funds()

