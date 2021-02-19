# encoding=utf8

__author__ = 'HLP'

import re
import datetime
import requests
from common import selects, excute_sql,  headers


def today():
    return datetime.datetime.now().strftime('%Y%m%d')


def get_fund_info(code_id):
    tengxun_url = "http://qt.gtimg.cn/"
    url_ = tengxun_url + "q=s_jj{fund_code}".format(fund_code=str(code_id))
    r = requests.get(url_, headers=headers)
    print(r.status_code, r.text)
    if r.status_code == 200:
        return r.text
    return


def get_update_funds_list():
    sql = "select * from fund_info where useful = '9';"
    return selects(sql)


def get_today_worth(code_id):
    text = get_fund_info(code_id)
    s = today() + "~(.+?)~"
    res_lst = re.findall(s, text)
    if res_lst:
        return res_lst[0]


def update_worth(worth, code_id):
    excute_sql("""update fund_info set worth_to_buy=%s where code_id='%s';""" % (str(worth), str(code_id)))
    excute_sql("""update fund_info set useful='2' where code_id='%s';""" % (str(worth), str(code_id)))


def main():
    fund_data = get_update_funds_list()
    for fund_dic in fund_data:
        code_id = fund_dic['code_id']
        worth = get_today_worth(code_id)
        update_worth(worth, code_id)


if __name__ == '__main__':
    main()