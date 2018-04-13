#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/12 0012 上午 6:29
 @Author  : Administrator
 @Software: PyCharm
 @Description:
"""

import hashlib
import os
from subprocess import Popen, PIPE

from jinja2 import Template


def calculate_hash(src):
    m2 = hashlib.md5()
    m2.update(str(src).encode("utf8"))
    return m2.hexdigest()


def render_gif(template_name, sentences):
    filename = template_name + "-" + calculate_hash(sentences) + ".gif"
    gif_path = "static/cache/gif/" + filename
    if os.path.exists(gif_path):
        return gif_path
    make_gif_with_ffmpeg(template_name, sentences, filename)
    return gif_path


def ass_text(template_name):
    with open("static/video/%s/template.tpl" % template_name) as fp:
        content = fp.read()
    return content.encode("utf-8")


def render_ass(template_name, sentences, filename):
    output_file_path = "static/cache/gif/%s.ass" % filename
    template = ass_text(template_name)
    rendered_ass_text = Template(template).render(sentences=sentences)
    with open(output_file_path, "w") as fp:
        fp.write(rendered_ass_text.encode("utf-8"))
    return output_file_path


def make_gif_with_ffmpeg(template_name, sentences, filename):
    ass_path = render_ass(template_name, sentences, filename)
    gif_path = "static/cache/gif/" + filename
    video_path = "static/video/" + template_name + "/template.mp4"
    cmd = "ffmpeg -i {video_path} -r 8 -vf ass={ass_path},scale=300:-1 -y {gif_path}" \
        .format(video_path=video_path, ass_path=ass_path, gif_path=gif_path)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.wait()
    if p.returncode != 0:
        print("Error.")
        return -1

if __name__ == '__main__':
    print(str(["hello"]))
    sentences = [u"好啊", u"就算你是一流工程师", u"就算你出报告再完美", u"我叫你改报告你就要改", u"毕竟我是客户", u"客户了不起啊", u"sorry 客户真的了不起", u"以后叫他天天改报告", u"天天改 天天改"]
    template_name = "sorry"
    path = render_gif(template_name, sentences)
    print(path)
