#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/12 0012 上午 7:06
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback

from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor

from lib.utils.logger_utils import logger
from scripts.render_gif_by_vedio import render_gif
from views.base import BaseHandler
import ujson as json


class GifHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @gen.coroutine
    def get(self, *args, **kwargs):
        pass


    @gen.coroutine
    def post(self, *args, **kwargs):
        try:
            interface = args[0]
            method_settings = {
                "generate/gif": self.generate_gif
            }
            response = yield method_settings[interface]()
            self.write(response)
            self.finish()
        except Exception, e:
            logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            self.write({"status": 0, "message": "操作失败"})

    @run_on_executor
    def generate_gif(self):
        gif_name = self.params.get("name")
        sentences = self.params.get("sentences")
        sentences = json.loads(sentences)
        path = render_gif(gif_name, sentences)
        return {"status": 0, "path": path}