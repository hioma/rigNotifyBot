# -*- coding: utf-8 -*-

import os
import sys
import time

from initialize import log

reload(sys)


# sys.setdefaultencoding('utf-8')


def notification_thread():
    while True:
        try:
            time.sleep(1)

        except Exception as e:
            log.error(
                '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                sys.exc_info()[2].tb_lineno,
                                                                os.path.basename(
                                                                    sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                sys._getframe().f_code.co_name,
                                                                e))
