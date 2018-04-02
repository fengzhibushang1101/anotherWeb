#coding=utf8
__author__ = 'changdongsheng'
from lib.sql2.joom_review import JoomReview
from lib.sql2.joom_pro import JoomPro
from lib.sql2.joom_user import JoomUser
from lib.sql2.joom_shop import JoomShop
from lib.sql2.product_body import ProductBody
from lib.sql2.task_schedule import TaskSchedule
from lib.sql2.category import Category
from lib.sql2.base import db, metadata


def create_all_tables():
    """
    创建所有表
    """
    metadata.create_all(bind=db)


if __name__ == "__main__":
    create_all_tables()