#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 上午 10:03
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback

from tornado import gen

from lib.utils.logger_utils import logger
from views.base import BaseHandler


class ApiHandler(BaseHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        try:
            interface = args[0]
            method_settings = {
                "jx3info": self.get_jx3info
            }
            response = yield method_settings[interface]()
            self.write(response)
            self.finish()

        except Exception, e:
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            self.write({"status": 0, "message": "获取失败"})


    def get_jx3info(self):
        pass


