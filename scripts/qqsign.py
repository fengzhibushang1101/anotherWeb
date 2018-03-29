#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/29 9:15
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import traceback
from time import sleep

import requests
from selenium import webdriver



headers = {"Content-Type":"application/x-www-form-urlencoded","Host":"qiandao.qun.qq.com","Origin":"http://qiandao.qun.qq.com","Referer": "http://qiandao.qun.qq.com","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"}

def get_cookies(qq, pwd):
    try:
        driver = webdriver.Chrome("C:\Users\yykj\Downloads\chromedriver_win32\chromedriver")
        driver.get('https://i.qq.com')
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        #填写QQ帐号
        driver.find_element_by_id('u').send_keys(qq)
        driver.find_element_by_id('p').clear()
        #填写QQ密码
        driver.find_element_by_id('p').send_keys(pwd)
        #模拟点击登录按钮 执行登录 获取cookie
        driver.find_element_by_id('login_button').click()
        sleep(10)
        cookies = driver.get_cookies()
        #退出浏览器
        driver.quit()
        return cookies
    except Exception, e:
        print traceback.format_exc(e)

def get_bkn(skey):
    e = 5381
    for i in range(len(skey)):
        e = e + (e << 5) + ord(skey[i])
    return str(2147483647 & e)


def sign(groupid, cookies):
    s = requests.Session()
    skey = ""
    for cookie in cookies:
        if cookie["name"] == "skey":
            skey = cookie['value']
        s.cookies.set(cookie['name'], cookie['value'])
    bkn = get_bkn(skey)
    s.cookies.set("Gtk", bkn)
    for gid in groupid:
        response = s.post("http://qiandao.qun.qq.com/cgi-bin/sign", data={"gc": gid, "is_sign": 0, "bkn": bkn},
                          headers=headers)
        print response.status_code
        print response.content
        responseJson = response.json()
        print responseJson
        if responseJson.has_key('em') and responseJson['em'] == 'no&nbsp;login':
            break
if __name__ == "__main__":
    """
        签到链接好像不可用了,有时间抓包看下请求是否有变化
    """
    qq = "714285795"
    pwd = "w251192185"
    groupids = [30935321]
    cookies = get_cookies(qq, pwd)


