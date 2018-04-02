#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 18:13
 @Author  : jyq
 @Software: PyCharm
 @Description:
"""
import functools
import random
import traceback

import requests
import time
from concurrent import futures


def get_joom_token():
    req_url = "https://www.joom.com/tokens/init"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-length": "0",
        "origin": "https://www.joom.com",
        "referer": "https://www.actneed.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "x-version": "0.1.0"
    }
    try_times = 3
    while try_times > 0:
        try:
            session = requests.session()
            res = session.post(req_url, headers=headers)
            result = res.json()
            return "Bearer %s" % result["accessToken"]
        except requests.ConnectTimeout:
            try_times -= 1
        except Exception, e:
            return False


def run_by_executor(thread_count, count):
    def executor_func(func):
        @functools.wraps(func)
        def wrapper(*args):
            with futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                task_dict = {
                    executor.submit(func, *args):
                        arg for arg in range(0, count)
                }
            for task in futures.as_completed(task_dict):
                args = task_dict[task]
                try:
                    task.result()
                    print("执行并发操作成功, 函数名称为 %s, 参数为%s" % (func.__name__, args))
                except Exception, e:
                    print(traceback.format_exc(e))
                    print("执行并发操作失败, 函数名称为 %s, 参数为%s" % (func.__name__, args))

        return wrapper
    return executor_func

if __name__ == "__main__":

    @run_by_executor(4, 20)
    def long_time_task(i):
        print('Run task %s (%s)...' % (i, i))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task %s runs %0.2f seconds.' % (i, (end - start)))

    for i in range(30):
        long_time_task(i)