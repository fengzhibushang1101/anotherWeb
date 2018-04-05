#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/5 0005 上午 8:27
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from tornado.websocket import WebSocketHandler


class WsHandler(WebSocketHandler):

    def open(self, *args, **kwargs):
        print "new client opened"

    def on_close(self):
        print "client closed"

    def on_message(self, message):
        self.write_message(message)