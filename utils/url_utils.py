#!/usr/bin/env python
# coding=utf-8
# created by junqiang.shen on 17-12-2
import json
import os
import re

import logging

import sys
from urllib import request

__author__ = 'junqiang.shen'


def parse_bilibili_live_room_id(url):
    # https://live.bilibili.com/(\d+).*
    if not url or isinstance(url, str) is False:  # only python2
        return

    pattern = re.compile(r'https?://live\.bilibili\.com/(\d+).*', re.I)
    m = pattern.match(url)
    if m:
        return m.group(1)


def response_json(url):
    if not url:
        return
    content = request.urlopen(url).read()

    if content:
        return json.loads(content.decode())


def download_stream(url, file_name):
    if not url:
        return

    res = None
    output_file = None

    try:
        res = request.urlopen(url, timeout=100000)
        output_file = open(file_name, 'wb')
        logging.info('starting download from:\n%s\nto:\n%s' % (url, file_name))

        size = 0
        _buffer = res.read(1024 * 256)
        while _buffer:
            output_file.write(_buffer)
            size += len(_buffer)
            sys.stdout.write('\r{:<4.2f} MB downloaded'.format(size/1024/1024))
            sys.stdout.flush()
            _buffer = res.read(1024 * 256)
    finally:
        if res:
            res.close()
        if output_file:
            output_file.close()

        if os.path.isfile(file_name) and os.path.getsize(file_name) == 0:
            os.remove(file_name)
