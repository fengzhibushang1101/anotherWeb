#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/2 19:53
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import sqlalchemy as SA
from sqlalchemy.ext.declarative import declarative_base

mysql_db = {
    "user": "myweb",
    "password": "MyNewPass4!",
    "host": "127.0.0.1",
    "db": "andata",
}
db = SA.create_engine(
    "mysql://%s:%s@%s/%s?charset=utf8mb4" % (mysql_db["user"], mysql_db["password"], mysql_db["host"], mysql_db["db"]),
    echo=False,
    pool_recycle=3600,
    pool_size=5000
)


Base = declarative_base()
metadata = Base.metadata