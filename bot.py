#!/usr/bin/env python
# -*- coding: utf-8 -*-

from initialize import *
import re
import os
import time
import string
from datetime import datetime
from threading import Thread
from threads import notification_thread
from tools import implode_new_lines, bot_send_message
import urllib2


def request_is_old(message):
    try:
        text = '<empty>'
        if message.text is not None:
            text = message.text

        if last_start_time > datetime.fromtimestamp(int(message.date)):
            log.info("received old message '{}' from @{}".format(implode_new_lines(text),
                                                                 message.chat.username))
            return True
        else:
            log.info("received new message '{}' from @{}".format(implode_new_lines(text),
                                                                 message.chat.username))
            return False
    except Exception as e:
        log.error(
            '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                            sys.exc_info()[2].tb_lineno,
                                                            os.path.basename(
                                                                sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                            sys._getframe().f_code.co_name,
                                                            e))
        return False


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    try:
        if request_is_old(message):
            return False

        answer = 'Привет, @{}!\n' \
                 'Данный бот умеет следить за тем ригом, на котором запущен. В данный момент есть поддержка' \
                 'Claymore\'s-майнеров. Бота я делаю под себя, но если вдруг у тебя есть идеи или вопросы, ' \
                 'то пиши @unknownplayer, попробуем что-нибудь сделать.\n' \
                 'Командуй /info, чтобы начать.'.format(message.chat.username)
        bot_send_message(message.chat.id, answer)
    except Exception as e:
        log.error(
            '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                            sys.exc_info()[2].tb_lineno,
                                                            os.path.basename(
                                                                sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                            sys._getframe().f_code.co_name,
                                                            e))


@bot.message_handler(commands=['info'])
def show_info(message):
    try:
        if request_is_old(message):
            return False

        answer = ''
        for miner in miners:
            response = urllib2.urlopen('http://{}:{}/'.format(miners[miner]['ip'], miners[miner]['port']))
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
                format_dict['hashrate_primary'] = format_dict['hashrates_gpus_primary'].split(';')[gpu_order_no]
                format_dict['hashrate_secondary'] = format_dict['hashrates_gpus_secondary'].split(';')[gpu_order_no]
                format_dict['temp'] = format_dict['temp_fans'].split(';')[gpu_num * 2]
                format_dict['fan'] = format_dict['temp_fans'].split(';')[gpu_num * 2 + 1]
                gpu_order_no += 1
                answer += miners[miner]['gpu_msg_format'].format(**format_dict)
            answer += miners[miner]['postfix_msg_format'].format(**format_dict)

        bot_send_message(message.chat.id, answer)
    except Exception as e:
        log.error(
            '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                            sys.exc_info()[2].tb_lineno,
                                                            os.path.basename(
                                                                sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                            sys._getframe().f_code.co_name,
                                                            e))


if __name__ == '__main__':
    queue_thread = notification_threads_array = None
    while True:
        try:
            last_start_time = datetime.now()
            log.info('starting bot in {}'.format(last_start_time))

            if notification_threads_array is None:
                notification_threads_array = []
                for i in range(1):
                    notification_threads_array.append(
                        Thread(target=notification_thread, name='NotificationThread{}'.format(i)))
                    notification_threads_array[i].daemon = True
                    notification_threads_array[i].start()

            bot.polling(none_stop=True)

            log.info('exiting with keyboard interrupt... wait 10 sec')
            time.sleep(10)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as main_e:
            log.error(
                '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                                sys.exc_info()[2].tb_lineno,
                                                                os.path.basename(
                                                                    sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                                sys._getframe().f_code.co_name,
                                                                main_e))
            time.sleep(10)
