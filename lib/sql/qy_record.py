#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/5/10 13:44
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""

import sqlalchemy as SA

from lib.sql.base import Base


class QiyuRecord(Base):
    __tablename__ = "qiyu_record"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    area_name = SA.Column(SA.String(16), nullable=False, default="")
    server_name = SA.Column(SA.String(16), nullable=False, default="")
    user_name = SA.Column(SA.String(16), nullable=False, default="")
    languages = SA.Column(SA.String(32), nullable=False, default="")
    qiyu_name = SA.Column(SA.String(32), nullable=False, default="")
    trigger_time = SA.Column(SA.INTEGER, nullable=False)
    first_share = SA.Column(SA.String(32), nullable=False, default="---")

    @classmethod
    def find_by_server_user_qiyu(cls, session, server_name, user_name, qiyu_name):
        return session.query(cls).filter(SA.and_(
            cls.server_name == server_name,
            cls.user_name == user_name,
            cls.qiyu_name == qiyu_name
        )).first()

