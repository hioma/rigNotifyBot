# -*- coding: utf-8 -*-

import time
import sys
import os
from datetime import datetime
from initialize import log, q
from tools import bot_send_message
from models import Users

reload(sys)
sys.setdefaultencoding('utf-8')


def queue_update_thread():
    while True:
        try:
            time.sleep(1)
            for user in Users.get_active():
                print 'added user to queue: ', user
                time.sleep(0.3)
                q.put(user)
            time.sleep(50)
        except Exception as e:
            log.error(
                '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                sys.exc_info()[2].tb_lineno,
                                                                os.path.basename(
                                                                    sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                sys._getframe().f_code.co_name,
                                                                e))


def notification_thread():
    while True:
        try:
            time.sleep(1)

            if not q.empty():
                user = q.get()

                print 'getted user: ', user
                time.sleep(3)
                q.task_done()
        except Exception as e:
            log.error(
                '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                sys.exc_info()[2].tb_lineno,
                                                                os.path.basename(
                                                                    sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                sys._getframe().f_code.co_name,
                                                                e))
