#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/22 0022 下午 9:11
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import parse_command_line
from tornado import gen

import logging
import tornadoredis
import json

from config import settings

logging = logging.getLogger('base.tornado')

# store clients in dictionary..
clients = dict()

REDIS_UPDATES_CHANNEL = 'chat'


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.client_id = None
        self._redis_client = None
        super(WebSocketHandler, self).__init__(*args, **kwargs)
        self._connect_to_redis()
        self._listen()

    def open(self, *args):
        self.client_id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.client_id] = self

    def on_message(self, message):
        """
        :param message (str, not-parsed JSON): data from client (web browser)
        """
        print("on message")

    @gen.coroutine
    def _on_update(self, message):
        """
        Receive Message from Redis when data become published and send it to selected client.
        :param message (Redis Message): data from redis
        """
        body = json.loads(message.body)
        if self.client_id == body['client_id']:
            self.write_message(message.body)

    @tornado.gen.engine
    def _listen(self):
        """
        Listening chanel 'REDIS_UPDATES_CHANNEL'
        """
        yield tornado.gen.Task(self._redis_client.subscribe, REDIS_UPDATES_CHANNEL)
        self._redis_client.listen(self._on_update)

    def on_close(self):
        """
        When client will disconnect (close web browser) then shut down connection for selected client
        """
        if self.client_id in clients:
            del clients[self.client_id]
            self._redis_client.unsubscribe(REDIS_UPDATES_CHANNEL)
            self._redis_client.disconnect()

    def check_origin(self, origin):
        """
        Check if incoming connection is in supported domain
        :param origin (str): Origin/Domain of connection
        """
        return True

    def _connect_to_redis(self):
        self._redis_client = tornadoredis.Client(host=settings.redis_host, port=settings.redis_port)
        self._redis_client.connect()


def main():
    parse_command_line()
    app = tornado.web.Application([
        (r'/socket', WebSocketHandler),
    ])
    app.listen(9999)
    print "the server is going to start..."
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
