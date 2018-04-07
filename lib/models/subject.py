#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/7 0007 下午 5:23
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from abc import ABCMeta, abstractmethod


class Subject():
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass
