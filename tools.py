# -*- coding: utf-8 -*-

import re
import urllib2
import time
from subprocess import call
from initialize import *


def implode_new_lines(text):
    return re.sub(r'[\r\n]+', r'\\n', text, re.UNICODE)


def bot_send_message(message_chat_id, message, reply_markup=None):
    log.debug(implode_new_lines(message))
    bot.send_message(message_chat_id, message, reply_markup=reply_markup)


def check_status_and_get_info():
    answer = ''
    for miner in miners:
        try:
            response = urllib2.urlopen('http://{}:{}/'.format(miners[miner]['ip'], miners[miner]['port']), timeout=3)
        except urllib2.URLError:
            status = 'miner \'{}\' freezes, try to restart all miners...'.format(miner)
            log.warn(status)
            call(settings['miners_kill_bat'])
            time.sleep(1)
            call(settings['miners_start_bat'])
            return status

        html = response.read()
        param_vals = re.search(miners[miner]['regex'], html)

        format_dict = {}
        for index, param_name in enumerate(miners[miner]['parsed_params']):
            format_dict[param_name] = param_vals.group(index + 1)

        answer += miners[miner]['prefix_msg_format'].format(**format_dict)

        gpu_order_no = 0
        for gpu_no in range(0, len(miners[miner]['di'])):
            gpu_num = int(miners[miner]['di'][gpu_no])
            format_dict['gpu_num'] = gpu_num
            hashrate_primary = format_dict['hashrates_gpus_primary'].split(';')[gpu_order_no]
            if hashrate_primary.isdigit():
                format_dict['hashrate_primary'] = float(hashrate_primary) / miners[miner]['divider']['primary']
            else:
                format_dict['hashrate_primary'] = 0
            hashrate_secondary = format_dict['hashrates_gpus_secondary'].split(';')[gpu_order_no]
            if hashrate_secondary.isdigit():
                format_dict['hashrate_secondary'] = float(hashrate_secondary) / miners[miner]['divider']['secondary']
            else:
                format_dict['hashrate_secondary'] = 0
            format_dict['temp'] = format_dict['temp_fans'].split(';')[gpu_num * 2]
            format_dict['fan'] = format_dict['temp_fans'].split(';')[gpu_num * 2 + 1]
            gpu_order_no += 1
            answer += miners[miner]['gpu_msg_format'].format(**format_dict)

        answer += miners[miner]['postfix_msg_format'].format(**format_dict)
    return answer