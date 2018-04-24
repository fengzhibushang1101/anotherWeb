#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/8 0008 下午 9:10
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import redis
from tornadoredis import Client

from config import settings
import ujson as json

redis_type = ["LIST", "DICT", "SET"]
pool = redis.ConnectionPool(host=settings.redis_host,
                            port=settings.redis_port,
                            db=settings.redis_db,
                            password=settings.redis_password,
                            max_connections=50)
conn = redis.Redis(connection_pool=pool, socket_timeout=60, charset='utf-8', errors='strict')

DEFAULT_EXPIRE = 60 * 60 * 2


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

    def incr(self, key, amount=1):
        return self.conn.incr(key, amount)

    def set_expiration(self, name, expiration):
        return self.conn.expire(name, expiration)

    def get_json(self, key):
        res = self.get(key)
        return json.loads(res) if res else None

    def set_cache(self, key, value, expiration=DEFAULT_EXPIRE):
        self.set(key, value)
        self.set_expiration(key, expiration=expiration)

    def set_json(self, key, value=""):
        value = json.dumps(value)
        self.set(key, value)

    def publish(self, channel, msg):
        self.conn.publish(channel, msg)
        return True

    def get_sub(self, channel):
        pub = self.conn.pubsub()
        pub.subscribe(channel)
        return pub

    def sadd(self, name, *key):
        try:
            return self.conn.sadd(name, *key)
        except Exception, e:
            print e
            return None

    def delete(self, name):
        return self.conn.delete(name)

    def sscan_iter(self, name, match=None, count=100, batch=500):
        cursor = '0'
        while cursor != 0:
            item_lst = []
            for i in xrange(count):
                cursor, data = self.conn.sscan(name, cursor=cursor,
                                      match=match, count=batch)
                if data:
                    item_lst.append(data)
                if cursor == 0:
                    break
            yield item_lst


def get_toredis_client():
    redis_client = Client(
            host=settings.redis_host,
            port=settings.redis_port,
            selected_db=settings.redis_db,
            password=settings.redis_password)
    redis_client.connect()
    return redis_client

redis_conn = RedisUtil()




if __name__ == "__main__":
    res = redis_conn.sadd("test_scan", *range(1500))
    print res
    # print redis_conn.get("a")
    c = redis_conn.sscan_iter("test_scan", batch=50, count=3)
    for d in c:
        print len(d)
        print d

redis_conn = RedisUtil()

# if __name__ == "__main__":
#     redis_conn.set("a", 1)
#     print redis_conn.get("a")