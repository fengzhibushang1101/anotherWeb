#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/8 0008 下午 9:10
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import redis

from config import settings

redis_type = ["LIST", "DICT", "SET"]
pool = redis.ConnectionPool(host=settings.redis_host,
                            port=settings.redis_port,
                            db=settings.redis_db,
                            password=settings.redis_password,
                            max_connections=50)
conn = redis.Redis(connection_pool=pool, socket_timeout=60, charset='utf-8', errors='strict')


class RedisUtil(object):

    def __init__(self):
        self.conn = conn

    def set(self, key, value=None):
        return self.conn.set(key, value)

    def get(self, key=None):
        return self.conn.get(key)

    def find_key(self, pattern):
        return self.conn.keys(pattern)

    def drop_key(self, key):
        if self.find_key(key):
            return self.conn.delete(key)

    def set_expiration(self, name, expiration):
        return self.conn.expire(name, expiration)


redis_conn = RedisUtil()

# if __name__ == "__main__":
#     redis_conn.set("a", 1)
#     print redis_conn.get("a")