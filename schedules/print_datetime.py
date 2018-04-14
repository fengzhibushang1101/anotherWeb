#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 下午 12:31
 @Author  : Administrator
 @Software: PyCharm
 @Description:
"""
import datetime

from lib.utils.logger_utils import logger
from schedules import scheduler


@scheduler.scheduled_job('interval', seconds=5)
def print_datetime():
    print datetime.datetime.now()
    logger.info(datetime.datetime.now())

