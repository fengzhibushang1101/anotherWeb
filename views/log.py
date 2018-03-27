#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 5:28
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback

from lib.sql.session import sessionCM
from lib.sql.user import User
from lib.utils.error_utils import NullArgumentException
from lib.utils.logger_utils import logger
from views.base import BaseHandler


class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.set_status(404, "invalid Path!")

    def post(self, *args, **kwargs):
        option = args[0]
        methods = {
            "in": self.log_in,
            "out": self.log_out
        }
        methods[option]()

    def log_in(self):
        mobile = self.params.get("mobile")
        pwd = self.params.get("pwd")
        mess = ""
        try:
            if not mobile or not pwd:
                raise NullArgumentException
            with sessionCM() as session:
                user = User.find_by_mobile(session, mobile)
                if not user:
                    mess = {"status": 0, "message": "用户不存在!"}
                else:
                    reg = user.check_password(pwd)
                    if not reg:
                        mess = {"status": 0, "message": "密码错误!"}
                    else:
                        self.session["user_id"] = user.id
                        self.set_cookie("MY_WEB", "true")
                        mess = {"status": 1, "message": "登陆成功!"}
        except NullArgumentException, e:
            mess = {"status": 0, "message": e.msg}
        except Exception, e:
            logger.error(traceback.format_exc(e))
            mess = {"status": 0, "message": "未知错误"}
        finally:
            self.write(mess)

    def log_out(self):
        self.session["user_id"] = None
        self.redirect("/")
