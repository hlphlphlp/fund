#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : HLP
# @File : common.py
# @Date : 2020/3/1 
# @Desc :

import pymysql

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.8(0x17000820) NetType/WIFI Language/zh_CN",
}

HOST = "127.0.0.1"
USER = "root"
PWD = "my@sql"

def connect(db='fund',host=HOST):
    try:
        conn = pymysql.connect(user=USER,
                                passwd=PWD,
                                host=host,
                                db=db,
                                charset='utf8')
    except pymysql.err.OperationalError as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    return conn

def insert(sql,db='fund'):
    """新增，
    例：sql=insert into 表名称 """
    conn = connect(db)
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()
    conn.close()

def excute_sql(sql,db='fund'):
    """新增，
    例：sql=insert into 表名称 """
    conn = connect(db)
    with conn.cursor() as cursor:
        cursor.execute(sql)
    conn.commit()
    conn.close()

def selects(sql,db='fund'):
    conn = connect(db)
    list = []
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    field = cur.description
    for i in range(len(result)):
        dic = {}
        for x in range(len(field)):
            dic[field[x][0]] = result[i][x]
        list.append(dic)
    cur.close()
    conn.close()
    return list

def select_field(field, table, condition={1:1}, db='fund'):
    """新增，
    例：sql=insert into 表名称 """
    conn = connect(db)
    sql = "select {field} from {table} where {condition}".format(field=field, table=table, condition=' and '.join([str(k)+"='"+str(v) + "'" for k,v in condition.items()]))
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
    conn.close()
    return result[0]


def send_mail(subject, contents):
    '''
    contents = ['This is the body, and here is just text http://somedomain/image.png',
                'You can find an audio file attached.', '/local/path/song.mp3']
    '''
    print("Start to send email:")
    import yagmail
    yag = yagmail.SMTP(user=select_field('user', 'mail_sender'), password=select_field('password', 'mail_sender'), host=select_field('host', 'mail_sender'))
    yag.send([select_field('email_address', 'mail_to', {'id': 1}), select_field('email_address', 'mail_to', {'id': 2})], subject, contents)
    print("Send email success !!!!!!!!")
    # yag.send([select_field('email_address', 'mail_to',{'id': 1})

