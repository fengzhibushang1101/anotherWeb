#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/28 0028 下午 8:55
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from celery import Celery  # windows下不要使用4以上的版本

celery = Celery()
celery.config_from_object('config.celeryconfig')
