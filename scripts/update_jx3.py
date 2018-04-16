#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 0015 下午 11:03
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

import requests

res = requests.post("http://localhost/api/jx3/info")

print res.content