#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : HLP
# @File : __init__.py.py
# @Date : 2020/2/8 
# @Desc :

import os, sys
current_path = os.getcwd()
base_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
print(base_dir)
sys.path.append(base_dir)
