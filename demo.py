#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : demo.py
# @Date : 2020/3/1 
# @Desc :


def select_field(field, table, condition={1:1}, db='fund'):
    """新增，
    例：sql=insert into 表名称 """
    # conn = connect(db)
    sql = "select {field} from {table} where {condition}".format(field=field, table=table, condition=' and '.join([str(k)+"='"+str(v) + "'" for k,v in condition.items()]))

    # with conn.cursor() as cursor:
    #     cursor.execute(sql)
    #     result = cursor.fetchone()
    # conn.close()
    print(sql)

select_field('content', 's_content', {'id': 1, 'name': 'nana'})