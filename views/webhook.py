#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 11:52
 @Author  : Administrator
 @Software: PyCharm
 @Description:
"""
from task.mail import send_mail
from views.base import BaseHandler


class WebHookHandler(BaseHandler):

    def post(self, *args, **kwargs):
        import subprocess
        cwd = "/root/src/anotherWeb"
        subprocess.Popen("git pull origin master; supervisorctl restart all; echo '更新成功!!!'", cwd=cwd, shell=True)
        send_mail.delay("git更新成功!", "网站更新成功!", to=["fengzhibushang@163.com"])

