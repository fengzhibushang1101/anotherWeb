#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:02
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""


import functools
import os.path
import traceback

import tornado.web

from lib.utils.logger_utils import logger


def  main():
    try:
    except Exception, e:
        print traceback.format_exc(e)
        logger.error(traceback.format_exc(e))