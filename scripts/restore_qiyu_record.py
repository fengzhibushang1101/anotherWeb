#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/10 14:45
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import random
import traceback

import requests
import time
from concurrent.futures import ThreadPoolExecutor

from lib.sql.jx3_server import Jx3Server
from lib.sql.qiyu_type import QiyuType
from lib.sql.qy_record import QiyuRecord
from lib.sql.session import sessionCM

url = u"https://jx3.derzh.com/serendipity/?m=1&test=1&R=%s&S=%s&t=&s=%s&n=&csrf=1805900225"


def exe_one_page(session, area_name, s_name, q_name):
    r_url = url % (area_name, s_name, q_name)
    print u"正在请求[ %s ][ %s ] 服务器 [ %s ]奇遇记录" % (area_name, s_name, q_name)
    res = requests.get(r_url)
    try:
        records = res.json().get("result", [])
        for record in records:
            QiyuRecord.create(session, **{
                'area_name': record.get("region"),
                'server_name': record.get("server"),
                'user_name': record.get("name"),
                'qiyu_name': record.get("serendipity", q_name),
                'trigger_time': record.get("time"),
                'first_share': record.get("report_name", "---")
            })

    except Exception, e:
        print res.content
        print "获取数据失败, 失败原因是:"
        print traceback.format_exc(e)


with sessionCM() as session:
    servers = Jx3Server.get_all_server(session)
    qiyus = QiyuType.get_all_qiyu_name(session)
    # with ThreadPoolExecutor(max_workers=32) as executor:
    for area_name, server_name, language in servers:
        for qiyu, languages in qiyus:
            if language in languages:
                exe_one_page(session, area_name, server_name, qiyu)
                time.sleep(random.randint(1, 5))

