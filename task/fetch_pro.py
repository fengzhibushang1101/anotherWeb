#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 0002 下午 8:26
 @Author  : jyq
 @Software: PyCharm
 @Description:
"""
import datetime
import traceback

import requests
from sqlalchemy import text

from lib.sql2.base import db
from lib.sql2.joom_pro import JoomPro
from lib.sql2.joom_shop import JoomShop
from lib.utils.logger_utils import logger
from task import celery
from task.func import get_joom_token
import ujson as json


def upsert_shop(connect, shop):
    try:
        sql = text('insert into joom_shop (joom_shop.name,shop_no,logo,rate,save_count,create_time,update_time,is_verify,pro_count,reviews_count,r_count_30,r_count_7,r_count_7_14,growth_rate,cate_id) values (:name,:shop_no,:logo,:rate,:save_count,:create_time,:update_time,:is_verify,0,0,0,0,0,0,"") on duplicate key update rate=:rate, save_count=:save_count, create_time=:create_time, update_time=:update_time, is_verify=:is_verify;')
        cursor = connect.execute(sql, **shop)
        cursor.close()
    except Exception, e:
        logger.info(traceback.format_exc(e))


def upsert_pro(connect, pro):
    try:
        sql = text('insert into joom_pro (joom_pro.name,pro_no,shop_no,category_id,image,rate,msrp,discount,real_price,reviews_count,create_time,update_time,cate_id1,cate_id2,cate_id3,cate_id4,cate_id5,origin_price,r_count_30,r_count_7,r_count_7_14,growth_rate,save_count) values (:name,:pro_no,:shop_no,:category_id,:image,:rate,:msrp,:discount,:real_price,:reviews_count,:create_time,:update_time,"","","","","",0,0,0,0,0,0) on duplicate key update joom_pro.name=:name,category_id=:category_id,rate=:rate,msrp=:msrp,discount=:discount,real_price=:real_price,reviews_count=:reviews_count,update_time=:update_time;')
        cursor = connect.execute(sql, **pro)
        cursor.close()
    except Exception, e:
        logger.info(traceback.format_exc(e))


def get_variants(variations):
    pro_vars = []
    for variation in variations:
        v_specifics = []
        if variation.get("colors"):
            v_specifics.append({
                "Image": [],
                "ValueID": variation["colors"][0].get("rgb", ""),
                "NameID": "",
                "Name": "Color",
                "Value": variation["colors"][0]["name"]
            })
        if variation.get("size"):
            v_specifics.append({
                "Image": [],
                "ValueID": "",
                "NameID": "",
                "Name": "Size",
                "Value": variation["size"]
            })
        pro_vars.append({
            "SkuID": variation["id"],  # 变体SKUID
            "PictureURL": "" if not variation.get("mainImage") else variation["mainImage"]["images"][3]["url"],
            "Active": variation["inStock"],
            "VariationSpecifics": v_specifics,  # 变体属性信息
            "Price": variation["price"],  # 价格
            "ShippingTime": "%s-%s" % (variation["shipping"]["maxDays"], variation["shipping"]["minDays"]),  # 运送时间
            "ShippingCost": variation["shipping"]["price"],  # 运费
            "MSRP": variation.get("msrPrice", 0),  # msrp
            "Stock": variation["inventory"]  # 库存
        })
    return pro_vars


def get_images(item):
    extra_images = [image["payload"]["images"][3]["url"] for image in item["gallery"] if image["type"] == "image"]
    main_image = item["mainImage"]["images"][3]["url"]
    return [main_image] + extra_images


def trans_pro(res):
    pro_data = dict()
    item = res["payload"]
    tag = item["id"]
    shop_data = item["store"]
    shop_info = {
        "name": shop_data["name"],
        "shop_no": shop_data["id"],
        "logo": "" if not shop_data.get("image") else shop_data["image"]["images"][3]["url"],
        "rate": shop_data.get("rating", 0),
        "is_verify": "1" if shop_data["verified"] else "0",
        "save_count": shop_data["favoritesCount"]["value"],
        "create_time": datetime.datetime.fromtimestamp(shop_data["updatedTimeMerchantMs"] / 1000),
        "update_time": datetime.datetime.fromtimestamp(shop_data["updatedTimeMerchantMs"] / 1000)
    }
    pro_info = {
        "name": item["name"],
        "pro_no": item["id"],
        "shop_no": item["storeId"],
        "category_id": item.get("categoryId", "0"),
        "image": item["mainImage"]["images"][3]["url"],
        "rate": item.get("rating", 0),
        "msrp": item["lite"].get("msrPrice", 0),
        "discount": item["lite"].get("discount", 0),
        "real_price": item["lite"]["price"],
        "reviews_count": item["reviewsCount"]["value"],
        "create_time": datetime.datetime.fromtimestamp(min(map(lambda z: z["createdTimeMs"], item["variants"])) / 1000),
        "update_time": datetime.datetime.fromtimestamp(
            max(map(lambda z: z["publishedTimeMs"], item["variants"])) / 1000)
        # 这里不准确
    }
    pro_info["r_count_30"] = pro_info["r_count_7"] = pro_info["r_count_7_14"] = pro_info["growth_rate"] = 0
    if item.get("categoryId"):
        print u"分类%s路径为%s" % (item["categoryId"], item["categoryId"])
        cate_path = ["0", "0", "0"]
        for index, path in enumerate(cate_path):
            pro_info["cate_id%s" % (index + 1)] = path
    parent_info = item["lite"]
    pro_data["SourceInfo"] = {
        "Platform": "Joom",
        "Link": "https://www.joom.com/en/products/%s/" % tag,
        "Site": "Global",
        "SiteID": 31,
        "ProductID": tag
    }
    pro_data["Title"] = item["name"]
    pro_data["rating"] = item.get("rating", 0)
    pro_data["reviews_count"] = item["reviewsCount"]
    pro_data["store_id"] = item["storeId"]
    pro_data["keywords"] = item.get("tags", [])
    pro_data["price"] = parent_info["price"]
    pro_data["MSRP"] = parent_info.get("msrPrice", 0)
    pro_data["discount"] = parent_info["discount"]
    pro_data["Description"] = item["description"]
    pro_data["ProductSKUs"] = list()
    pro_data["images"] = get_images(item)
    pro_data["ProductSKUs"] = get_variants(item["variants"])
    return pro_data, shop_info, pro_info


@celery.task(ignore_result=True)
def fetch_pro(tag, token, connect):
    data_url = 'https://api.joom.com/1.1/products/%s?language=en-US&currency=USD' % tag
    res = requests.get(data_url, headers={"authorization": token})
    if "unauthorized" in res.content:
        token = get_joom_token()
        fetch_pro.delay(tag, token)
        return
    content = json.loads(res.content)
    pro_data, shop_info, pro_info = trans_pro(content)
    upsert_shop(connect, shop_info)
    upsert_pro(connect, pro_info)
    logger.info(u"产品%s保存成功!" % tag)

