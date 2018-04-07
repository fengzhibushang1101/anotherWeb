#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/5 0005 上午 8:27
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import urllib
from uuid import uuid4

import datetime
from tornado.websocket import WebSocketHandler, WebSocketClosedError

from lib.controls.chat_home import ChatHome
from lib.models.observer import Observer
from views.base import BaseHandler

chat_home = ChatHome()


class WsHandler(WebSocketHandler, Observer, BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(WsHandler, self).__init__(application, request, **kwargs)
        self.info = {"female": "default", "name": self.current_user.name or self.current_user.mobile, 'u_id': uuid4()}

    def check_origin(self, origin):
        # parsed_origin = urllib.parse.urlparse(origin)
        # return parsed_origin.netloc.endswith()
        return True

    def open(self, *args, **kwargs):
        chat_home.add(self)

    def on_close(self):
        chat_home.remove(self)

    def on_message(self, message):
        chat_home.notify({"from": self.info["u_id"], "message": message, "name": self.info["name"]})

    def update(self, mess):
        u_id = mess["from"]
        trans_mess = dict(
            message=mess["message"],
            name=mess.get("name"),
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        if u_id == self.info['u_id']:
            trans_mess["type"] = "self"
        elif u_id == "0":
            trans_mess["type"] = "sys"
        else:
            trans_mess["type"] = "other"
        try:
            self.write_message(trans_mess)
        except WebSocketClosedError:
            chat_home.remove(self)
