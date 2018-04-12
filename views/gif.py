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

from lib.sql.gif_list import GifList
from lib.sql.session import sessionCM
from lib.utils.logger_utils import logger
from scripts.render_gif_by_vedio import render_gif
from views.base import BaseHandler
import ujson as json
from tornado.web import HTTPError


class GifHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    def get(self, *args, **kwargs):
        name = args[0]
        render_settings = self.gen_render_settings()
        with sessionCM() as session:
            gif_info = GifList.find_by_name(session, name)
            print
            if not gif_info:
                raise HTTPError(404)
            render_settings["name"] = name
            render_settings["length"] = gif_info.length
        self.render("gif/sorry.html", **render_settings)

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
        return {"status": 1, "path": path}