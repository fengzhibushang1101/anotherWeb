#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/7 0007 下午 5:34
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler, authenticated


class ChatHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        render_settings = self.gen_render_settings()
        self.render("chat/chat.html", **render_settings)

    @authenticated
    def post(self, *args, **kwargs):
        pass
