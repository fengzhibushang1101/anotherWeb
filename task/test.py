#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 0002 下午 8:44
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from task.fetch_cate_pro import fetch_cate_pro
from task.fetch_cate import fetch_cate
from task.fetch_review import fetch_review

if __name__ == "__main__":
    # fetch_review.delay("1490346955899457642-241-1-26341-2083628188", "123")
    fetch_cate.delay("1")
    # fetch_cate_pro.delay("1", "1473502947527000494-66-2-118-3090934056")