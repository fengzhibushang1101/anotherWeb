#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 1:19
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        print self.current_user
        self.render("index/index.html")

    def post(self, *args, **kwargs):
        pass
