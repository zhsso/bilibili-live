#!/usr/bin/env python
# coding=utf-8
# created by junqiang.shen on 17-12-3
from multiprocessing.pool import Pool

import time

import logging

from api.bilibili import Bilibili

__author__ = 'junqiang.shen'


def monitor_master(pool, room_id_set):
    bilibili = Bilibili()

    recoding_id = set()
    while True:
        for item in room_id_set:
            if item in recoding_id:
                continue

            _room_id = bilibili.get_live_room_id(room_id=item)
            room_info = bilibili.get_room_info(_room_id)

            if room_info and room_info['data']['live_status'] == 1:
                recoding_id.add(item)
                pool.apply_async(recording_live, (bilibili, _room_id))
            else:
                time.sleep(30)


def recording_live(bilibili, room_id):
    try:
        bilibili.download_stream(room_id)
    except TimeoutError:
        logging.error('recoding room_id:%s is failed' % room_id)

if __name__ == '__main__':
    download_pool = Pool(4)
    monitor_master(download_pool, set([63129, 37799]))
