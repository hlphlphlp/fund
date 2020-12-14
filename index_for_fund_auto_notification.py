#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : index_for_fund_auto_notification.py
# @Date : 2020/2/18 
# @Desc :

import requests
import operator
from datetime import datetime
from common import selects, send_mail, select_field
from store_shanghai_index import get_value_from_tengxun_info
from fund_assessment import get_fund_assessment

def generat_mail_text(result_dic):
    result_content = '''
    {name}, 代码: {id}
    当   前: {current_value}
    今日最高: {today_highest}
    今日最低: {today_lowest}
    与昨收盘相比: {compare_to_yesterday}    涨/降幅度:  {amplitude} %
    
    昨   收: {yesterday_end}
    今   开: {today_begin}
    成交量:  {deal_count}亿手         成交额:  {deal_money}亿
    买入参考：成交量1~2.4亿手，成交额900~2700亿
    ===============================
                   估值  一周  一月↑
    '''.format(name=result_dic['name'], id=result_dic['id'], current_value=result_dic['current_value'], yesterday_end=result_dic['yesterday_end'],
               today_begin=result_dic['today_begin'], today_highest=result_dic['today_highest'], today_lowest=result_dic['today_lowest'], amplitude=result_dic['amplitude'],
               deal_count=result_dic['deal_count'], deal_money=result_dic['deal_money'], compare_to_yesterday=result_dic['compare_to_yesterday'])
    return result_content

def strategy_content():
    content = '''
    ===============================
%s
    ''' % select_field('content', 's_content', {'id': 3})
    return content


def compare_3000_history_value(index_value, days = select_field('content', 's_content', {'id': 2})):
    offset = float(select_field('content', 's_content', {'id': 4}))
    sql = "select yesterday_end from shanghai_index order by update_time desc limit %s;" % str(days)
    r = selects(sql)
    print("yesterday_end: " + str(r))
    flag = True
    if (index_value - offset) > float(r[0]['yesterday_end']):
        flag = False
    else:
        for dic in r:
            if index_value > float(dic['yesterday_end']):
                flag = False
    # 如果一天内猛跌70点
    if float(r[0]['yesterday_end']) - index_value >= 70:
        flag = True
    # 如果两天内猛跌120点
    if float(r[1]['yesterday_end']) - index_value >= 120:
        flag = True
    print("compare_3000_history_value Flag: " + str(flag))
    return flag

def compare_4000_history_value(index_value, days= select_field('content', 's_content', {'id': 2})):
    sql = "select yesterday_end from shanghai_index order by update_time desc limit %s;" % str(days)
    r = selects(sql)
    print("yesterday_end: " + str(r))
    flag = True
    for dic in r:
        if index_value < float(dic['yesterday_end']):
            flag = False
    # 如果一天内猛涨120点
    if index_value - float(r[0]['yesterday_end']) >= 120:
        flag = True
    # 如果两天内猛涨200点
    if index_value - float(r[0]['yesterday_end']) >= 200:
        flag = True
    print("compare_4000_history_value Flag: " + str(flag))
    return flag

def specil_strategy(mode='low'):
    low_assessment = select_field('low', 'index_line', {'id': 3})
    high_assessment = select_field('high', 'index_line', {'id': 3})
    my_fund = select_my_fund(mode='fund')
    assessment_result = get_result_fund_lst(fund_data=my_fund, sort_key='assessment')
    if mode == 'low':
        if assessment_result[0]['assessment'] <= low_assessment: return True
        else: return False
    elif mode == 'high':
        if assessment_result[-1]['assessment'] >= high_assessment: return True
        else: return False
    else:
        return False

def send_email_notice(index_value, content):
    low_index1 = select_field('low', 'index_line', {'id': 1})
    high_index1 = select_field('high', 'index_line', {'id': 1})
    low_index2 = select_field('low', 'index_line', {'id': 2})
    high_index2 = select_field('high', 'index_line', {'id': 2})
    index_value_float = float(index_value)

    if (index_value_float < low_index2 and specil_strategy(mode='low')) or (index_value_float < low_index1 and compare_3000_history_value(index_value_float)):
        subject = '快来【买入】基金啦！今日上证指数低谷 = %s！' % str(index_value_float)
        send_mail(subject, content)
        print(index_value + " < %s send email success" % str(low_index1))
    elif (index_value_float > high_index2 and specil_strategy(mode='high')) or (index_value_float > high_index1 and compare_4000_history_value(index_value_float)):
        subject = '快来【卖出】基金啦！今日上证指数趋于高峰 > %s！' % str(index_value_float)
        send_mail(subject, content)
        print(index_value + " > %s send email success" % str(high_index1))
    elif '买' in content[2] or '卖' in content[2]:
        subject = '快来快来，某基金呼喊你'
        send_mail(subject, content)
        print('快来快来，某基金呼喊你')

def select_fund_seek_bank(mode='fund'):
    sql = "select * from {mode}_info where useful >= '1';".format(mode=mode)
    return selects(sql)

def select_my_fund(mode='fund'):
    sql = "select * from {mode}_info where useful = '2';".format(mode=mode)
    return selects(sql)


def get_fund_increase_info(fund_code):
    tengxun_url = "http://web.ifzq.gtimg.cn"
    url_ = tengxun_url + "/fund/newfund/fundBase/getRankInfo"
    jjstring = 'jj' + str(fund_code)
    params = {'symbol': jjstring}
    r = requests.get(url_, params=params)
    # print(r.status_code, r.text)
    if r.status_code == 200 and r.json()['code'] == 0:
        return r.json()
    return {"data":{"zxrq":"2020-00-00","total":0,"jzzf":{"w1":0,"w4":0,"w13":0,"w26":0,"w52":0,"year":0,"total":0,"year3":0}}}

def change_fund_increase_dic(fund_code, fund_name):
    '''
    {"code":0,"msg":"OK","data":{"zxrq":"2020-02-18","total":2110,"jzzf":{"w1":5.06,"w4":9.68,"w13":20.5,"w26":37.51,"w52":83.41,"year":18.37,"total":261.5,"year3":138.77},"avg_hbl":{"w1":0,"w4":0,"w13":0,"w26":0,"w52":0,"year":0,"total":0,"year3":0},"jz_rank":{"w1":"709","w4":"376","w13":"494","w26":"338","w52":"69","year":"328","total":"140","year3":"6"},"ratio_level":{"w1":2,"w4":1,"w13":1,"w26":1,"w52":1,"year":1,"total":1,"year3":1}}}
    :param fund_code:
    :return: {'one_week': 5.06, 'one_month': 9.68, 'three_month': 20.5}
    '''
    result_dic = {}
    fund_increase_info = get_fund_increase_info(fund_code)
    result_dic['code_id'] = fund_code
    result_dic['fund_name'] = fund_name
    result_dic['assessment'] = float(get_fund_assessment(fund_code)['assessment_rate'])    #加估值
    result_dic['assessment_worth'] = float(get_fund_assessment(fund_code)['assessment_worth'])  # 加预估净值
    result_dic['one_week'] = fund_increase_info['data']['jzzf']['w1']
    result_dic['one_month'] = fund_increase_info['data']['jzzf']['w4']
    result_dic['three_month'] = fund_increase_info['data']['jzzf']['w13']
    result_dic['six_month'] = fund_increase_info['data']['jzzf']['w26']
    result_dic['one_year'] = fund_increase_info['data']['jzzf']['w52']
    result_dic['three_year'] = fund_increase_info['data']['jzzf']['year3']
    print(result_dic)
    return result_dic

def get_result_fund_lst(fund_data, sort_key='assessment'):
    result_lst = []
    for data_dic in fund_data:
        fund_increase_dic = change_fund_increase_dic(data_dic['code_id'], data_dic['name'])
        if data_dic['worth_to_buy'] and fund_increase_dic['assessment_worth'] < data_dic['worth_to_buy']:
            fund_increase_dic['fund_name'] = '【买买买】' + fund_increase_dic['fund_name']
        if data_dic['worth_to_sell'] and fund_increase_dic['assessment_worth'] > data_dic['worth_to_sell']:
            fund_increase_dic['fund_name'] = '【卖卖卖】' + fund_increase_dic['fund_name']
        fund_increase_dic.pop('code_id')
        fund_increase_dic.pop('three_month')
        fund_increase_dic.pop('six_month')
        fund_increase_dic.pop('one_year')
        fund_increase_dic.pop('three_year')
        fund_increase_dic.pop('assessment_worth')
        result_lst.append(fund_increase_dic)
    sorted_result_lst = sorted(result_lst, key=operator.itemgetter(sort_key))
    return sorted_result_lst

def get_mail_fund_content(mode='fund'):
    fund_data = select_fund_seek_bank(mode)
    print("fund_data===========" + str(fund_data))
    result_fund_bank_lst = get_result_fund_lst(fund_data, sort_key='one_month')
    print("result_fund_bank_lst===========" + str(result_fund_bank_lst))
    result_fund_bank_content = '\n'.join([' '.join([str(v) for v in x.values()]) for x in result_fund_bank_lst])
    return result_fund_bank_content

def get_avg_index_last_days(days):
    sql = "select avg(y.yesterday_end) AVG,max(y.yesterday_end) MAX,min(y.yesterday_end) MIN from (select yesterday_end from shanghai_index order by update_time desc limit {days}) as y;".format(days=days)
    res = selects(sql)
    return res[0]

def avg_content(days = select_field('content', 's_content', {'id': 5})):
    res = get_avg_index_last_days(days)
    content = '''
    最近 {somedays} 天的平均值：{avg}
    最小值：{min}   最大值：{max}
    
    '''.format(avg=res['AVG'], min=res['MIN'], max=res['MAX'], somedays=days)
    print(content)
    return content

def main():
    print("Today's date: " + str(datetime.now()))
    # 股票基金
    result_fund_bank_content = get_mail_fund_content(mode='fund')
    # 债券基金
    result_stock_bank_content = get_mail_fund_content(mode='stock')
    result_dic = get_value_from_tengxun_info()
    index_content = generat_mail_text(result_dic)
    print("generat_mail_text success!")
    dividing_line = '''
    -----------------债券基金-----------------'''
    send_email_notice(result_dic['current_value'], [avg_content(), index_content, result_fund_bank_content, dividing_line, result_stock_bank_content, strategy_content()])
    print(result_fund_bank_content)
    print(index_content)
    print(result_stock_bank_content)
    print(strategy_content())

def main2():
    '''
    每日估算净值监控
    '''
    res = selects("select code_id, name from fund_info where worth is not null")


if __name__ == '__main__':
    main()

