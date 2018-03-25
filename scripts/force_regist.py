#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 10:41
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""


"""
额, 本来想通过比较暴力的方法去强行注册actneed账户, 结果发现注册部分只做了前台验证,没有做后台验证,直接就注册成功,很尴尬!
"""
import requests

def gen_verify_code(length=4):
    for x in xrange(0, int(('{:0<%s}' % (length+1)).format('1'))):
        yield "%%0%sd" % length % x


# for i in gen_verify_code(4):
res = requests.post("https://www.actneed.com/register", params={
    "mobile": "18111111",
    "password": "123123123"
})
print res.content

