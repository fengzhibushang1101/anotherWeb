#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 5:28
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

from views.base import BaseHandler

visitor_id = 0


class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.set_status(404, "invalid Path!")

    def post(self, *args, **kwargs):
        option = args[0]
        methods = {
            "in": self.log_in,
            "out": self.log_out
        }
        methods[option]()

    def log_in(self):
        global visitor_id
        if not self.get_secure_cookie("MW"):
            self.set_secure_cookie("MW",  self.params.get("name", "游客%s" % visitor_id))
            visitor_id += 1
        self.write({"status": 1, "message": "登陆成功"})

    def log_out(self):
        self.set_secure_cookie("MW", "")
        self.redirect("/")
