#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 11:52
 @Author  : Administrator
 @Software: PyCharm
 @Description:
"""


from views.base import BaseHandler


class WebHookHandler(BaseHandler):

    def post(self, *args, **kwargs):
        import subprocess
        cwd = "/root/src/anotherWeb"
        subprocess.Popen("git pull origin master; supervisorctl restart all; echo '更新成功!!!' | mail -s '项目更新成功!!!' fengzhibushang@163.com", cwd=cwd, shell=True)

