#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/22 15:46
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""

import paramiko
import re

# 设置主机列表
host_list = [{'ip': '47.254.16.204', 'port': 22, 'username': 'odin', 'password': 'Ww#251192185'}]

ssh = paramiko.SSHClient()
# 设置为接受不在known_hosts 列表的主机可以进行ssh连接
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in host_list:
    try:
        ssh.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        print(host['ip'])
        stdin, stdout, stderr = ssh.exec_command('cat /proc/meminfo')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue

        str_total = re.search('MemTotal:.*?\n', str_out).group()
        print(str_total)
        totalmem = re.search('\d+', str_total).group()
        print totalmem
        str_free = re.search('MemAvailable:.*?\n', str_out).group()
        print(str_free)
        availablemem = re.search('\d+', str_free).group()
        use = 1 - round(float(availablemem) / float(totalmem), 100)
        print('当前内存使用率为：' + str(use))

        stdin, stdout, stderr = ssh.exec_command('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()

        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle1 = cpu_time_list[3]
            total_cpu_time1 = 0
            for t in cpu_time_list:
                total_cpu_time1 = total_cpu_time1 + int(t)

        time.sleep(2)

        stdin, stdout, stderr = ssh.exec_command('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle2 = cpu_time_list[3]
            total_cpu_time2 = 0
            for t in cpu_time_list:
                total_cpu_time2 = total_cpu_time2 + int(t)

        cpu_usage = round(1 - (float(cpu_idle2) - float(cpu_idle1)) / (total_cpu_time2 - total_cpu_time1), 2)
        print('当前CPU使用率为：' + str(cpu_usage))

        ssh.close()
    except Exception, e:
        print e
        print 123
