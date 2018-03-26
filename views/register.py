#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 11:52
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback

from lib.sql.session import sessionCM
from lib.sql.user import User
from lib.utils.error_utils import NullArgumentException, ErrorArgumentError
from lib.utils.logger_utils import logger
from views.base import BaseHandler


class RegisterHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.write_error(404)

    def post(self, *args, **kwargs):
        self.write(self.add_new_user())

    def add_new_user(self):
        try:
            mobile = self.params.get("mobile")
            password = self.params.get("password")
            password2 = self.params.get("password2")
            if not mobile or not password:
                raise NullArgumentException
            if password != password2:
                raise ErrorArgumentError
            with sessionCM() as session:
                user = User.find_by_mobile(session, mobile)
                if user:
                    return {"status": 0, "message": "用户已存在"}
                else:
                    user = User.create(session, mobile, password)
                    self.set_secure_cookie("MW", "游客%s" % user.id)
                    return {"status": 1, "message": "注册成功!"}
        except NullArgumentException, e:
            return {"status": 0, "message": e.msg}
        except ErrorArgumentError, e:
            return {"status": 0, "message": e.msg}
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return {"status": 0, "message": "these is something wrong!"}