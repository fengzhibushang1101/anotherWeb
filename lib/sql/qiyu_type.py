#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/10 12:04
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import sqlalchemy as SA

from lib.sql.base import Base


class QiyuType(Base):

    __tablename__ = "qiyu_type"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    qy_type = SA.Column(SA.String(16), nullable=False, default="")
    qy_name = SA.Column(SA.String(16), nullable=False, default="")
    languages = SA.Column(SA.String(32), nullable=False, default="")

    @classmethod
    def get_all_qiyu_name(cls, session):
        records = session.query(cls.qy_name, cls.languages).all()
        return [(record.qy_name, record.languages) for record in records]
