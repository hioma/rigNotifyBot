# -*- coding: utf-8 -*-

import os
import sys
import time

from config import settings
from initialize import log, q
from models import Users
from tools import bot_send_message, get_miners_info

reload(sys)
sys.setdefaultencoding('utf-8')


def passive_notification_queue_update_thread():
    if not settings['passive_notification_timeout'] == 0:
        while True:
            try:
                time.sleep(1)
                for user in Users.get_active():
                    q.put((user, get_miners_info()))
                time.sleep(settings['passive_notification_timeout'])
            except Exception as e:
                log.error(
                    '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                    sys.exc_info()[2].tb_lineno,
                                                                    os.path.basename(
                                                                        sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                    sys._getframe().f_code.co_name,
                                                                    e))


def active_notification_queue_update_thread():
    if not settings['active_notification_timeout'] == 0:
        while True:
            try:
                time.sleep(1)
                for user in Users.get_active():
                    bad_events_info = get_miners_info(do_active=True)
                    if not bad_events_info == '':
                        q.put((user, bad_events_info))
                    else:
                        log.info('no alerts detected')
                time.sleep(settings['active_notification_timeout'])
            except Exception as e:
                log.error(
                    '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                    sys.exc_info()[2].tb_lineno,
                                                                    os.path.basename(
                                                                        sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                    sys._getframe().f_code.co_name,
                                                                    e))


def messages_send_thread():
    while True:
        try:
            if not q.empty():
                (user, msg_text) = q.get()
                log.info('send some message to @{}'.format(user['telegram_nickname']))
                bot_send_message(user['chat_id'], msg_text)
                q.task_done()

            time.sleep(1)
        except Exception as e:
            log.error(
                '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                sys.exc_info()[2].tb_lineno,
                                                                os.path.basename(
                                                                    sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                sys._getframe().f_code.co_name,
                                                                e))
