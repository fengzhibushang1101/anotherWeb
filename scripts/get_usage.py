#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/22 15:46
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""

import paramiko
import re

# 设置主机列表
host_list = ({'ip': '180.76.57.10', 'port': 22, 'username': 'root', 'password': '#w251192185'})

ssh = paramiko.SSHClient()


