#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 上午 10:10
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from lib.nosql.redis_util import redis_conn

class Jx3Info(object):

    BATTLEGROUND_ORDER = [["云湖天池", 10], ["三国古战场", 15]]
    REDIS_KEY = "jx3_current"

    def get_info(self):
        pass

    def set_info(self):
        pass