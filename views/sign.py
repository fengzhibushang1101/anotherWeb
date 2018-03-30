#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/30 0030 下午 10:27
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler


class SignHandler(BaseHandler):

    def get(self, *args, **kwargs):
        option = args[0]
        render_settings = self.gen_render_settings()
        self.render("index/sign%s.html" % option, **render_settings)