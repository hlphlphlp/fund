# encoding=utf8

__author__ = 'HLP'


from common import selects, excute_sql


def get_funds_list():
    sql = "select * from fund_info where worth_to_buy is not null;"
    return selects(sql)


def update_auto_update_is_9(code_id):
    excute_sql("""update fund_info set useful='9' where code_id='%s';""" % (str(worth), str(code_id)))


def main():
    fund_data = get_funds_list()
    for fund_dic in fund_data:
        code_id = fund_dic['code_id']
        update_auto_update_is_9(code_id)
