#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @File : store_lucky_numbers.py
# @Desc : 
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
from fund.common import insert


def generate_list(number):
    return [i + 1 for i in range(number)]


def generate_diff_numbers(number_list, count):
    import random
    res_list = []
    for i in range(count):
        lucky_number = random.choice(number_list)
        # print(lucky_number)
        res_list.append(lucky_number)
        number_list.remove(lucky_number)
        # print(number_list)
    return res_list


def main():
    blue_number_list = generate_list(35)
    blue_lucky_numbers = generate_diff_numbers(blue_number_list, 5)
    red_number_list = generate_list(12)
    red_lucky_numbers = generate_diff_numbers(red_number_list, 2)
    blue_lucky_numbers.sort()
    red_lucky_numbers.sort()
    print(blue_lucky_numbers, red_lucky_numbers)
    insert(sql='''INSERT INTO lucky_numbers (`date`, `blue`, `red`)
                                VALUES
                                    (
                                        CURRENT_DATE,
                                        '{blue_numbers}',
                                        '{red_numbers}'
                                    );'''.format(blue_numbers=str(blue_lucky_numbers), red_numbers=str(red_lucky_numbers)), db='daletou')


if __name__ == '__main__':
    main()
