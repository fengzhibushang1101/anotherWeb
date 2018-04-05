#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/4 16:22
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler


class EsHandler(BaseHandler):


    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "text/event-stream")
        self.flush("111111111111111111")
        self.finish()

    def post(self, *args, **kwargs):
        pass

