#!/usr/bin/env python
# coding=utf-8
# created by junqiang.shen on 17-12-2
import logging

import time

import subprocess

from api.core.core import Core
from utils.url_utils import parse_bilibili_live_room_id, response_json, download_stream

__author__ = 'junqiang.shen'


class Bilibili(Core):
    _API0 = 'http://space.bilibili.com/ajax/live/getLive?mid='
    _API1 = 'http://live.bilibili.com/api/player?id=cid:'
    _API2 = 'http://live.bilibili.com/live/getInfo?roomid='  # obsolete
    _API3 = 'http://live.bilibili.com/api/playurl?cid='  # obsolete
    _API4 = 'https://api.live.bilibili.com/room/v1/Room/room_init?id='
    _API5 = 'http://api.live.bilibili.com/room/v1/Room/get_info?room_id='
    _API6 = 'http://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid='
    _API7 = 'https://api.live.bilibili.com/api/playurl?otype=json&platform=web&cid='

    def __init__(self):
        pass

    def get_live_room_id(self, room_id=None, live_url=None, uid=None):
        if room_id:  # 输入的是主播空间直播介绍房间号,一般比较长
            return response_json(Bilibili._API4 + str(room_id))['data']['room_id']
        elif live_url:  # 输入的是直播页面地址
            room_id = parse_bilibili_live_room_id(live_url)

            try:
                return response_json(Bilibili._API4 + room_id)['data']['room_id']
            except KeyError as e:
                logging.error('get room_id failed:%s' % str(e))
        elif uid:
            pass
        else:
            logging.error('get room_id failed:both live_url and uid is null')

    def get_stream_url(self, room_id):
        try:
            response = response_json(Bilibili._API7 + str(room_id))
            return response['durl'][0]['url']
        except KeyError as e:
            logging.error('get room_info failed:', e)

    def login(self):
        pass

    def get_room_info(self, room_id):
        try:
            return response_json(Bilibili._API5 + str(room_id))
        except KeyError as e:
            logging.error('get room_info failed:', e)

    def get_anchor_info(self, room_id):
        try:
            return response_json(Bilibili._API6 + str(room_id))
        except KeyError as e:
            logging.error('get anchor_info failed:', e)

    def download_stream(self, room_id, file_name=None):
        _url = self.get_stream_url(room_id)

        if not file_name:
            _anchor_info = self.get_anchor_info(room_id)
            file_name = '{name}_{time}.flv'.format(name=_anchor_info['data']['info']['uname'], time=time.time())
        download_stream(_url, file_name)

    def stream_player(self, room_id):
        _url = self.get_stream_url(room_id)
        subprocess.run(['mpv', _url])
