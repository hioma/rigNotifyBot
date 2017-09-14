# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import urllib2

from telebot import types

from initialize import log, bot, miners_settings, settings, q
from models import Users

previous_hasrates = {}


def implode_new_lines(text):
    return re.sub(r'[\r\n]+', r'\\n', text, re.UNICODE)


def bot_send_message(message_chat_id, message, reply_markup=None):
    if reply_markup is None:
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        reply_markup.add(
            types.KeyboardButton('/info'),
            types.KeyboardButton('/reboot'),
            types.KeyboardButton('/pause'),
            types.KeyboardButton('/donate'),
        )
    log.debug('sended message to {} chat: '.format(message_chat_id, implode_new_lines(message)))
    bot.send_message(message_chat_id, message, reply_markup=reply_markup)


def send_messages_to_all_active(message, reply_markup=None):
    log.debug('sended message to all active: '.format(implode_new_lines(message)))
    for user in Users.get_active():
        q.put((user, message))


def run_subprocess(proc_path):
    subprocess.call([settings['subprocess_windows_crutch'], proc_path])


def get_miners_info(do_active=False):
    try:
        answer = ''
        new_hashrates = {}
        for miner in miners_settings:
            try:
                response = urllib2.urlopen('http://{}:{}/'.format(miners_settings[miner]['ip'], miners_settings[miner]['port']), timeout=miners_settings[miner]['timeout'])
            except Exception:
                status = 'Майнер \'{}\' не запущен или завис :(\n'.format(miner)
                if not do_active:
                    answer += status
                    continue
                else:
                    status += 'Запускаем \'miner_freezes_or_not_runnig\'-скрипт'
                    log.warn(implode_new_lines(status))
                    run_subprocess(miners_settings[miner]['miner_freezes_or_not_runnig'])
                    return status

            html = response.read()
            param_vals = re.search(miners_settings[miner]['regex'], html)

            format_dict = {}
            for index, param_name in enumerate(miners_settings[miner]['parsed_params']):
                format_dict[param_name] = param_vals.group(index + 1)

            answer += miners_settings[miner]['prefix_msg_format'].format(**format_dict)

            gpu_order_no = 0
            for gpu_no in range(0, len(miners_settings[miner]['di'])):
                gpu_num = int(miners_settings[miner]['di'][gpu_no])
                format_dict['gpu_num'] = gpu_num
                hashrate_primary = format_dict['hashrates_gpus_primary'].split(';')[gpu_order_no]
                if hashrate_primary.isdigit():
                    format_dict['hashrate_primary'] = float(hashrate_primary) / miners_settings[miner]['divider']['primary']
                    if miner not in new_hashrates:
                        new_hashrates[miner] = []
                    new_hashrates[miner].append(format_dict['hashrate_primary'])
                else:
                    format_dict['hashrate_primary'] = 0
                hashrate_secondary = format_dict['hashrates_gpus_secondary'].split(';')[gpu_order_no]
                if hashrate_secondary.isdigit():
                    format_dict['hashrate_secondary'] = float(hashrate_secondary) / miners_settings[miner]['divider']['secondary']
                    if miner not in new_hashrates:
                        new_hashrates[miner] = []
                    new_hashrates[miner].append(format_dict['hashrate_secondary'])
                else:
                    format_dict['hashrate_secondary'] = 0
                if gpu_num * 2 in format_dict['temp_fans'].split(';'):
                    format_dict['temp'] = format_dict['temp_fans'].split(';')[gpu_num * 2]
                else:
                    format_dict['temp'] = 'NaN'
                if gpu_num * 2 + 1 in format_dict['temp_fans'].split(';'):
                    format_dict['fan'] = format_dict['temp_fans'].split(';')[gpu_num * 2 + 1]
                else:
                    format_dict['fan'] = 'NaN'
                gpu_order_no += 1
                answer += miners_settings[miner]['gpu_msg_format'].format(**format_dict)

            answer += miners_settings[miner]['postfix_msg_format'].format(**format_dict)
        if not do_active:
            return answer
        else:
            status = ''
            global previous_hasrates
            for miner in previous_hasrates:
                if miners_settings[miner]['hashrate_fall_percentage'] > 0:
                    for i, previous_hasrate in enumerate(previous_hasrates[miner]):
                        if previous_hasrate > 0:
                            percent = 100.0 - float(new_hashrates[miner][i]) / previous_hasrate * 100
                            if percent >= miners_settings[miner]['hashrate_fall_percentage']:
                                status = ('Хэшрейт \'{}\'#{} упал на {:0.0f}%, запускаем \'hashrate_falled\' скрипт\n'
                                          'Предыдущие данные:\n{}' ).format(miner, i + 1, percent, answer)
                                log.warn(implode_new_lines(status))
                                run_subprocess(miners_settings[miner]['miner_freezes_or_not_runnig'])
                                break
            previous_hasrates = new_hashrates.copy()
            return status
    except Exception as e:
        log.error(
            '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                            sys.exc_info()[2].tb_lineno,
                                                            os.path.basename(
                                                                sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                            sys._getframe().f_code.co_name,
                                                            e))
        return 'Error: unknown exception in \'get_miners_info\' :('
