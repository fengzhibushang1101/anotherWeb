#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from sqlalchemy import text

from lib.sql2.base import db
from lib.sql2.joom_review import JoomReview
from lib.sql2.joom_user import JoomUser
from lib.sql2.session import sessionCM
from lib.utils.logger_utils import logger
from task import celery
from task.func import get_joom_token
import ujson as json


def upsert_review(session, review):
    logger.info(u"正在插入评论, no为%s" % review["review_no"])
    try:
        session.excute(JoomReview.__table__.insert(), review)
    except Exception, e:
        pass


def upsert_user(session, user):
    logger.info(u"正在插入用户, no为%s" % user["user_no"])
    try:
        session.excute(JoomUser.__table__.insert(), user)
    except Exception, e:
        pass

def retrieve_review(reviews_info):
    try:
        review_users = []
        review_datas = []
        now_dt = datetime.datetime.now()
        moment_30 = int(time.mktime((now_dt - datetime.timedelta(days=30)).timetuple())) * 1000
        moment_14 = int(time.mktime((now_dt - datetime.timedelta(days=14)).timetuple())) * 1000
        moment_7 = int(time.mktime((now_dt - datetime.timedelta(days=7)).timetuple())) * 1000
        rc30 = len(filter(lambda a: a["createdTimeMs"] > moment_30, reviews_info))
        rc7 = len(filter(lambda a: a["createdTimeMs"] > moment_7, reviews_info))
        rc714 = len(filter(lambda a: moment_14 < a["createdTimeMs"] < moment_7, reviews_info))
        if rc714:
            growth_rate = (float(float(rc7) / rc714) - 1) * 100
        else:
            growth_rate = 0
        review_count = {"r_count_30": rc30, "r_count_7": rc7, "r_count_7_14": rc714, "growth_rate": growth_rate}
        for review in reviews_info:
            review_data = {
                "review_no": review["id"],
                "create_time": datetime.datetime.fromtimestamp(review["createdTimeMs"] / 1000),
                "update_time": datetime.datetime.fromtimestamp(review["updatedTimeMs"] / 1000),
                "pro_no": review["productId"],
                "variation_id": review["productVariantId"],
                "user_no": review["user"]["id"] if review.get("user") else "",
                "language": review.get("originalLanguage", ""),
                "origin_text": review.get("originalText", ""),
                "new_text": review.get("text", ""),
                "order_id": review.get("orderId", ""),
                "is_anonymous": review["isAnonymous"],
                "colors": json.dumps(review["productVariant"]["colors"]) if review["productVariant"].get("colors") else "",
                "star": review["starRating"],
                "shop_no": review["productLite"]["storeId"],
                "photos": ""
            }
            if review.get("user"):
                user_data = {
                    "full_name": review["user"].get("fullName", ""),
                    "user_no": review["user"]["id"],
                    "images": review["user"]["avatar"]["images"][0]["url"] if review["user"].get("avatar") else ""
                }
                review_users.append(user_data)
            review_datas.append(review_data)
        return review_datas, review_users, review_count
    except Exception as e:
        logger.error(traceback.format_exc(e))
        raise Exception("reviewer error")


@celery.task(ignore_result=True)
def fetch_review(tag, token, page_token=None):
    url = "https://api.joom.com/1.1/products/%s/reviews?=all&count=1000&sort=top&language=en-US&currency=USD" % tag
    params = {
        "filter_id": "all",
        "count": 500,
        "sort": "top"
    }
    if page_token:
        params["pageToken"] = page_token
    logger.info(u"正在第%s次抓取产品%s的评论, 参数为%s" % (1,  tag, params))
    res = requests.get(url, params=params, headers={"authorization": token})
    if "unauthorized" in res.content:
        token = get_joom_token()
        fetch_review.delay(tag, token, page_token)
        return
    content = res.json()
    if content.get("payload"):
        reviews = content["payload"]["items"]
        review_datas, review_users, review_count = retrieve_review(reviews)
        with sessionCM() as session:
            for rev_pro in review_datas:
                upsert_review(session, rev_pro)
            for r_user in review_users:
                upsert_user(session, r_user)
            session.commit()
        # with futures.ThreadPoolExecutor(max_workers=16) as executor:
        #     future_to_pro = {
        #         executor.submit(upsert_review, connect=connect, review=rev_pro): rev_pro for rev_pro in review_datas
        #     }
        #     for future in futures.as_completed(future_to_pro):
        #         rev_pro = future_to_pro[future]
        #         try:
        #             rp = future.result()
        #         except Exception as exc:
        #             logger.error("%s generated an exception: %s" % (rev_pro, exc))
        # with futures.ThreadPoolExecutor(max_workers=16) as executor:
        #     future_to_user = {
        #         executor.submit(upsert_user, connect=connect, user=r_user): r_user for r_user in review_users
        #     }
        #     for future in futures.as_completed(future_to_user):
        #         r_user = future_to_user[future]
        #         try:
        #             ru = future.result()
        #         except Exception as exc:
        #             logger.error("%s generated an exception: %s" % (r_user, exc))

        if content["payload"].get("nextPageToken") and len(reviews):
            return fetch_review.delay(tag, token, page_token=content["payload"]["nextPageToken"])
    else:
        logger.info(u"抓取产品%s的评论失败, 参数为%s" % (tag, params))



