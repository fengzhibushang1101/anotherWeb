#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 0002 下午 8:26
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.sql2.category import Category
from task.fetch_cate_pro import fetch_cate_pro

"""
 @Time    : 2018/4/2 0002 下午 8:26
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import datetime
import time
import traceback

import requests
from concurrent import futures

from lib.sql2.base import db
from lib.sql2.joom_review import JoomReview
from lib.sql2.joom_user import JoomUser
from lib.utils.logger_utils import logger
from task import celery
from task.func import get_joom_token
import ujson as json


@celery.task(ignore_result=True)
def fetch_cate(token, p_tag=None, level=1, p_id=0):
    url = 'https://api.joom.com/1.1/categoriesHierarchy'
    params = {'levels': 1, 'parentLevels': 1, 'language': 'en-US', 'currency': 'USD'}
    if p_tag:
        params["categoryId"] = p_tag
    logger.info(u"正在采集id为%s的分类" % p_tag)
    logger.info(u"参数为%s" % params)
    res = requests.get(url, params=params, headers={"authorization": token})
    if "unauthorized" in res.content:
        token = get_joom_token()
        fetch_cate.delay(token, p_tag, level, p_id)
        return
    n_level = level + 1
    if res.status_code == 200:
        content = json.loads(res.content)
        c_infos = content["payload"]["children"]
        for c_info in c_infos:
            tag = c_info['id']
            name = c_info['name']
            is_leaf = 0 if c_info["hasPublicChildren"] else 1
            cate = Category.raw_save(tag, name, p_id, is_leaf, level, 31)
            n_p_id = cate
            if not is_leaf:
                fetch_cate.delay(token, p_tag=tag, level=n_level, p_id=n_p_id)
            else:
                fetch_cate_pro.delay(token, tag)



