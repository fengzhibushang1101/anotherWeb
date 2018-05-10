#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/10 12:02
 @Author  : jyq
 @Software: PyCharm
 @Description:
"""
from lib.sql.base import Base
import sqlalchemy as SA


class Jx3Server(Base):
    __tablename__ = "jx3_server"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    area_name = SA.Column(SA.String(16), nullable=False, default="")
    server_name = SA.Column(SA.String(16), nullable=False, default="")
    language = SA.Column(SA.String(16), nullable=False, default="")

    @classmethod
    def get_all_server(cls, session):
        records = session.query(cls.area_name, cls.server_name, cls.language).all()
        return [(record.area_name, record.server_name, record.language) for record in records]
