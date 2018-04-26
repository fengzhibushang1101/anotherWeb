#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 0002 下午 8:26
 @Author  : jyq
 @Software: PyCharm
 @Description:
"""

import requests
from concurrent import futures

from lib.sql2.base import db
from lib.sql2.session import sessionCM
from lib.utils.logger_utils import logger
from task import celery
from task.fetch_review import fetch_review
from task.fetch_pro import fetch_pro
from task.func import get_joom_token, random_key
import ujson as json


@celery.task(ignore_result=True)
def fetch_cate_pro(token, cate_id, pgToken=None, times=1):
    url = 'https://api.joom.com/1.1/search/products?language=en-US&currency=USD&_=jfs3%s'
    params = {
        'count': 50,
        'filters': [{
            'id': 'categoryId',
            'value': {
                'type': 'categories',
                'items': [{
                    'id': cate_id
                }]
            }
        }]
    }
    if pgToken:
        params["pageToken"] = pgToken
    logger.info(u"正在抓取分类%s下第%s页产品" % (cate_id, times))
    res = requests.post(url % random_key(4), data=json.dumps(params), headers={
        "authorization": token,
        "content-type": 'application/json'
    })
    if "unauthorized" in res.content:
        token = get_joom_token()
        fetch_cate_pro.delay(token, cate_id, pgToken, times)
        return

    content = json.loads(res.content)
    items = content["payload"]["items"]
    if len(items) == 0:
        logger.info(u"分类%s抓取完成!" % cate_id)
    else:
        for item in items:
            logger.info(u'产品id为%s' % item["id"])
            fetch_review.delay(item["id"], token)
        with futures.ThreadPoolExecutor(max_workers=32) as executor:
            future_to_user = {
                executor.submit(fetch_pro, tag=item["id"], token=token): item["id"] for item in items
            }
            for future in futures.as_completed(future_to_user):
                rev_pro = future_to_user[future]
                try:
                    rp = future.result()
                except Exception as exc:
                    logger.error("%s generated an exception: %s" % (rev_pro, exc))
        if "nextPageToken" in content["payload"]:
            fetch_cate_pro.delay(token, cate_id, content["payload"]["nextPageToken"], times+1)



