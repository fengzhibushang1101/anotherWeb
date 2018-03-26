#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:25
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""



# log configure
import os

LOG_PATH = '/logs/myweb/'
LOG_FILE = os.path.sep.join([LOG_PATH, 'myweb.log'])
DEFAULT_LOG_SIZE = 1024*1024*50

# mysql configure
ECHO_SQL = False

DB = {
    "user": "myweb",
    "password": "MyNewPass4!",
    "host": "127.0.0.1",
    "db_name": "myweb",
}
