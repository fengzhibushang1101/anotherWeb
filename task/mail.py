#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/28 0028 下午 8:55
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from task import celery


@celery.task
def send_mail(mail):
    print('sending mail to %s...' % mail['to'])
    print('mail sent.')