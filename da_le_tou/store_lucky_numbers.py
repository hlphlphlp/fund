#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @File : store_lucky_numbers.py
# @Desc : 
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
from fund.common import insert
import random


def generate_list(number):
    return [i + 1 for i in range(number)]


def generate_diff_numbers_basic(number_list, count):
    import random
    res_list = []
    for i in range(count):
        lucky_number = random.choice(number_list)
        # print(lucky_number)
        res_list.append(lucky_number)
        number_list.remove(lucky_number)
        # print(number_list)
    return res_list


def generate_diff_numbers_special(number_list, count):
    import random
    res_list = []
    for i in range(count):
        temp_list = [x for x in number_list if x not in res_list]
        # print("temp_list: " + str(temp_list))
        while len(temp_list) > 1:
            pop_number = random.choice(temp_list)
            # print("pop_number: " + str(pop_number))
            temp_list.remove(pop_number)
        res_list.append(temp_list[0])
    return res_list


def generate_diff_numbers_mixed(number_list, count):
    import random
    res_list = []
    for i in range(count):
        lucky_number, = random.choice([generate_diff_numbers_basic(number_list, 1), generate_diff_numbers_special(number_list, 1)])
        res_list.append(lucky_number)
        # print(number_list)
    return res_list


def main():
    blue_number_list = generate_list(34)
    blue_lucky_numbers = random.choice([generate_diff_numbers_basic(blue_number_list, 5), generate_diff_numbers_special(blue_number_list, 5), generate_diff_numbers_mixed(blue_number_list, 5)])
    red_number_list = generate_list(11)
    red_lucky_numbers = random.choice([generate_diff_numbers_basic(red_number_list, 2), generate_diff_numbers_special(red_number_list, 2), generate_diff_numbers_mixed(red_number_list, 2)])
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
