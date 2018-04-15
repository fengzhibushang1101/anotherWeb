#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 上午 10:10
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import ujson as json
from redis import RedisError, WatchError

from lib.nosql.redis_util import redis_conn as redis
from lib.sql.jx3_daily_record import Jx3DailyRecord
from lib.sql.session import sessionCM
from lib.utils.time_utils import Timer
from task.mail import send_to_master


class Jx3Info(object):
    BATTLEGROUND_ORDER = [["云湖天池", 10], ["三国古战场", 15], ["浮香丘", 15], ["坑爹之路", 25], ["神农洇", 15], ["九宫棋谷", 25]]
    REDIS_KEY = "jx3_current"
    TIME_KEY = "jx3_update_time"

    @classmethod
    def get_info(cls):
        current = redis.get(cls.REDIS_KEY)
        return cls.BATTLEGROUND_ORDER[int(current) % len(cls.BATTLEGROUND_ORDER)]

    @classmethod
    def set_info(cls, value):
        with redis.conn.pipeline() as pipe:
            with sessionCM() as session:
                try:
                    pipe.watch(cls.REDIS_KEY, cls.TIME_KEY)
                    pipe.multi()
                    redis.set(cls.REDIS_KEY, value)
                    time = Timer.now_time()
                    redis.set(cls.TIME_KEY, time)
                    pipe.execute()
                    Jx3DailyRecord.create(session, update_time=time, info=json.dumps(cls.get_info()))
                except WatchError:
                    pipe.reset()

    @classmethod
    def auto_add_one(cls):
        last_time = redis.get(cls.TIME_KEY)
        if not Timer.is_in_yesterday(last_time):
            send_to_master("剑网三自动更新出错", "上次更新时间错误!")
            return False
        with redis.conn.pipeline() as pipe:
            with sessionCM() as session:
                try:
                    pipe.watch(cls.REDIS_KEY, cls.TIME_KEY)
                    pipe.multi()
                    res = redis.incr(cls.REDIS_KEY)
                    if not res:
                        raise RedisError
                    time = Timer.now_time()
                    redis.set(cls.TIME_KEY, Timer.now_time())
                    pipe.execute()
                    Jx3DailyRecord.create(session, update_time=time, info=json.dumps(cls.get_info()))
                except WatchError:
                    pipe.reset()


if __name__ == "__main__":
    print Jx3Info.set_info(0)
    print Jx3Info.get_info()
