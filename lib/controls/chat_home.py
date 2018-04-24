#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/7 0007 下午 5:04
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import ujson as json
from lib.nosql.redis_util import redis_conn, get_toredis_client

CHAT_CHANNEL = "CHAT"

class ChatHome(object):

    def __init__(self):
        self.registers = set()
        self.client = get_toredis_client()

    def add(self, register):
        self.registers.add(register)
        message = u'用户%s加入聊天室' % register.info["name"]
        self.notify({"from": "0", "message": message}, self.count)

    def count(self, msg):
        message = u'当前聊天室共有%s名成员' % msg
        self.notify({"from": "0", "message": message})

    def remove(self, register):
        self.registers.remove(register)
        message = u'用户%s离开聊天室' % register.info["name"]
        self.notify({"from": "0", "message": message})
    #
    # def receive_message(self, info):
    #     self.notify(info)

    def __len__(self):
        return self.counts

    @property
    def counts(self):
        return len(self.registers)

    def notify(self, mess, callback=None):
        self.client.publish(CHAT_CHANNEL, json.dumps(mess), callback)
        # for register in self.registers:
        #     register.update(mess)
