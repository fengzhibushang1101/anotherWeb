#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/31 0031 上午 9:58
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler, authenticated


class ProjectHandler(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        print args
        print self.settings
        project_name = args[0]
        render_settings = self.gen_render_settings()
        self.render("../project/{0}/index.html".format(project_name), **render_settings)