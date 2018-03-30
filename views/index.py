#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 1:19
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler, authenticated


class IndexHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        render_settings = self.gen_render_settings()
        self.render("index/index.html", **render_settings)

    @authenticated
    def post(self, *args, **kwargs):
        pass
