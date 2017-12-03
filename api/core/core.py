#!/usr/bin/env python
# coding=utf-8
# created by junqiang.shen on 17-12-2

__author__ = 'junqiang.shen'


class Core:
    def login(self):
        raise NotImplementedError()

    def get_live_room_id(self, live_url, uid):
        """
        通过网页直播页面url或者主播的uid获取直播房间号
        :param live_url: 主播直播网页url地址
        :param uid: 主播注册对应的uid,可以在主播主页查看
        :return:
        """
        raise NotImplementedError()

    def get_room_info(self, room_id):
        raise NotImplementedError()

    def get_stream_url(self, room_id):
        raise NotImplementedError()

    def get_anchor_info(self, room_id):
        raise NotImplementedError()

    def download_stream(self, room_id, file_name):
        raise NotImplementedError()

    def stream_player(self, room_id):
        raise NotImplementedError()
