#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:02
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""


import os.path
import traceback

import sys
from tornado import ioloop, web, options, httpserver

from config import settings
from lib.utils.logger_utils import logger
from views.index import IndexHandler

options.define('port', default=8080, type=int)



SETTINGS = dict(
    template_path=os.path.join(os.path.dirname(sys.argv[0]), "templates"),
    static_path=os.path.join(os.path.dirname(sys.argv[0]), "static"),
    login_url="/",
)



urls = [
    (r'/', IndexHandler)
]


def main():
    try:
        options.parse_command_line()
        port = options.options.port
        settings.configure('PORT', port)
        app = web.Application(handlers=urls, debug=True, **SETTINGS)
        server = httpserver.HTTPServer(app)
        server.listen(settings.port)
        print "the server is going to start..."
        print "http://localhost:%s/" % options.options.port
        ioloop.IOLoop().instance().start()

        # app = tornado.wsgi.WSGIApplication(
        #     handlers=urls, debug=True,
        #     **SETTINGS
        # )
        # server = gevent.wsgi.WSGIServer(('', settings.port), app)
        # server.serve_forever()
    except Exception, e:
        print traceback.format_exc(e)
        logger.error(traceback.format_exc(e))


if __name__ == "__main__":
    main()