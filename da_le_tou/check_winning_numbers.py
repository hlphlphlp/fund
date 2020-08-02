#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @File : draw_wining_numbers.py
# @Desc : 

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
from fund.common import selects
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    r = requests.get(url)
    if r.status_code == 200 and r.text:
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    else: return


def query_wining_numbers():
    res_wining_numbers = {}
    winning_numbers_history_url = 'http://datachart.500.com/dlt/history/history.shtml'
    soup = get_soup(winning_numbers_history_url)
    tr_tree_list = soup.find(id='tdata').find_all(name='tr')
    for tr in tr_tree_list:
        blue_list = [int(tree.string) for tree in tr.find_all(attrs={'class': 'cfont2'})]
        # print(blue_list)

        red_list = [int(tree.string) for tree in tr.find_all(attrs={'class': 'cfont4'})]
        # print(red_list)

        other_list = [tree.string for tree in tr.find_all(attrs={'class': 't_tr1'})]
        # print(other_list)

        res_wining_numbers[other_list[-1]] = {'blue': blue_list, 'red': red_list}
    # print(res_wining_numbers)
    return res_wining_numbers


def verify(lotto_blue, lotto_red):
    '''
    1、完全相同
    2、
    :param lotto_blue:
    :param lotto_red:
    :return:
    '''
    my_numbers = selects(sql='select date,blue,red from lucky_numbers', db='daletou')
    for luck in my_numbers:
        luck_blue_count = 0
        luck_red_count = 0
        for i in lotto_blue:
            if i in eval(luck['blue']):
                luck_blue_count += 1
        for i in lotto_red:
            if i in eval(luck['red']):
                luck_red_count += 1
        if luck_blue_count == 5 and luck_red_count == 2:
            print("一等奖！")
            print(luck)
        elif luck_blue_count == 5 and luck_red_count == 1:
            print("二等奖！")
            print(luck)
        elif luck_blue_count == 5:
            print("三等奖！")
            print(luck)
        elif luck_blue_count == 4 and luck_red_count == 2:
            print("四等奖！")
            print(luck)
        elif luck_blue_count == 4 and luck_red_count == 1:
            print("五等奖！")
            print(luck)
        elif luck_blue_count == 4 or (luck_blue_count == 3 and luck_red_count == 2):
            print("六等奖！")
            print(luck)
        elif (luck_blue_count == 2 and luck_red_count == 2) or (luck_blue_count == 3 and luck_red_count == 1):
            print("七等奖！")
            print(luck)
        elif luck_blue_count == 3 or luck_red_count == 2 or (luck_blue_count == 2 and luck_red_count == 1) or (luck_blue_count == 1 and luck_red_count == 2):
            print("八等奖！")
            print(luck)


if __name__ == '__main__':
    winning_numbers = query_wining_numbers()
    verify(winning_numbers['2020-08-01']['blue'], winning_numbers['2020-08-01']['red'])
