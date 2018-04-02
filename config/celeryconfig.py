#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/28 0028 下午 8:45
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from kombu import Queue, Exchange
CELERY_DEFAULT_QUEUE = "default_queue"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default.queue"
CELERY_IGNORE_RESULT = True
CELERY_ACKS_LATE = True
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_RESULT_BACKEND = "amqp"
CELERY_EVENT_QUEUE_TTL = 10
CELERY_EVENT_QUEUE_EXPIRES = 10
CELERY_SEND_EVENTS = False
CELERYD_PREFETCH_MULTIPLIER = 2
# CELERYD_TASK_TIME_LIMIT = 3 * 10 * 60
# BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3 * 6 * 10 * 60}
# CELERYD_MAX_TASK_PER_CHILD = 500  # 内存泄漏时开启




CELERY_QUEUES = (
    Queue('default_queue', Exchange('default_queue'), routing_key='default_queue'),
    Queue('send_mail', Exchange('mail'), routing_key='send.mail', exchange_type="direct"),
    # Queue('fetch_review', Exchange('fetch_review'), routing_key='fetch_joom.fetch_review', exchange_type="direct"),
    # Queue('fetch_cate', Exchange('fetch_cate'), routing_key='fetch_joom.fetch_cate', exchange_type="direct"),
    # Queue('fetch_cate_pro', Exchange('fetch_cate_pro'), routing_key='fetch_joom.fetch_cate_pro', exchange_type="direct"),
    # Queue('fetch_pro', Exchange('fetch_pro'), routing_key='fetch_joom.fetch_pro', exchange_type="direct"),
)

CELERY_ROUTES = (
    # 发送邮件的队列
    {"task.mail.send_mail": {"routing_key": "send.mail", "queue": "send_mail"}},
    # 抓取review队列
    # {"task.fetch_review.fetch_review": {"routing_key": "fetch_joom.fetch_review", "queue": "fetch_review"}},
    # # 抓取category队列
    # {"task.fetch_cate.fetch_cate": {"routing_key": "fetch_joom.fetch_cate", "queue": "fetch_cate"}},
    # # 抓取分类产品队列
    # {"task.fetch_cate_pro.fetch_cate_pro": {"routing_key": "fetch_joom.fetch_cate_pro", "queue": "fetch_cate_pro"}},
    # # 抓取产品队列
    # {"task.fetch_pro.fetch_pro": {"routing_key": "fetch_joom.fetch_pro", "queue": "fetch_pro"}},
)
#
# CELERYBEAT_SCHEDULE = {
#
# }
#
CELERY_IMPORTS = (
    "task.mail",
    # "task.fetch_review",
    # "task.fetch_cate",
    # "task.fetch_cate_pro",
    # "task.fetch_pro"
)

CELERY_SEND_TASK_ERROR_EMAILS = False

# if env in ["production"]:
#     BROKER_URL = 'amqp://myweb:w251192185@180.76.98.136:5672/myweb'
# else:
BROKER_URL = 'amqp://myweb:w251192185@localhost:5672/myweb'
