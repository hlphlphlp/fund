#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : monetary_fund.py
# @Date : 2020/2/8 
# @Desc :

import requests
from bs4 import BeautifulSoup

fund_dic = {
    "000621": "易方达现金增利货币 - B	",
    "002753": "建信嘉薪宝货币B	",
    "000836": "国投瑞银钱多宝货币A	",
    "000837": "国投瑞银钱多宝货币I	",
    "001234": "国金众赢货币	",
    "003712": "泰达宏利京元宝货币B	",
    "000759": "平安财富宝货币	",
    "001821": "兴全天添益货币B	",
    "003465": "平安金管家货币	",
    "519517": "汇添富货币B	",
    "001909": "创金合信货币A	",
    "003483": "交银施罗德天鑫宝货币E	",
    "003388": "招商招益宝货币A	",
    "003389": "招商招益宝货币B	",
    "004179": "圆信永丰丰润货币B	",
    "004869": "中融日日盈交易型货币B	",
    "004972": "长城收益宝货币A	",
    "004973": "长城收益宝货币B	",
    "005151": "红土创新优淳货币B	",
    "005097": "易方达现金增利货币 - C	"
}

def get_fund_html(fund_id):
    headers = {"Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
               }
    url = "http://fund.eastmoney.com/%s.html?spm=search" % str(fund_id)
    # print(url)
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_7_rate(soup):
    fund_info = soup.find(attrs={'class': 'dataItem02'})
    return fund_info.dd.text

def get_14_rate(soup):
    fund_info = soup.find(attrs={'class': 'dataItem03'})
    return fund_info.dd.text

def get_28_rate(soup):
    fund_info = soup.find(attrs={'class': 'dataItem04'})
    return fund_info.dd.text

def get_funds_rate(fund_dic, function=get_7_rate):
    res_dic = {}
    for fund_id in fund_dic.keys():
        soup = get_fund_html(fund_id)
        rate = function(soup)
        res_dic[fund_id + " - " + fund_dic[fund_id]] = rate
    # print(res_dic)
    print("===================================", function.__name__)
    return res_dic

def sort(res_dic):
    fund_name_lst = []
    for key in sorted(res_dic, key=res_dic.__getitem__, reverse=True):
        print(key, " ：", res_dic[key])
        fund_name_lst.append(key)
    return fund_name_lst

def ranking_7_14_28():
    res_dic = {}
    res_dic_7 = get_funds_rate(fund_dic, get_7_rate)
    ranking_7_lst = sort(res_dic_7)
    res_dic_14 = get_funds_rate(fund_dic, get_14_rate)
    ranking_14_lst = sort(res_dic_14)
    res_dic_28 = get_funds_rate(fund_dic, get_14_rate)
    ranking_28_lst = sort(res_dic_28)
    print("======================================== ranking_7_14_28")
    for i in range(len(ranking_7_lst)):
        fund_name = ranking_7_lst[i]
        index_14 = ranking_14_lst.index(fund_name)
        index_28 = ranking_28_lst.index(fund_name)
        res_dic[fund_name] = sum([i, index_14, index_28])
    for key in sorted(res_dic, key=res_dic.__getitem__):
        print(key, " ：", res_dic_7[key], res_dic_14[key], res_dic_28[key])

if __name__ == '__main__':
    # 计算7、14、28天的个别rate排名情况
    # res_dic = get_funds_rate(fund_dic, get_28_rate)
    # sort(res_dic)

    # 计算7、14、28天总体rate排名情况
    ranking_7_14_28()
