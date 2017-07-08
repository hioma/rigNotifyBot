# -*- coding: utf-8 -*-

import re
import urllib2
import subprocess
from initialize import log, bot, miners_settings, settings

previous_hasrates = {}


def implode_new_lines(text):
    return re.sub(r'[\r\n]+', r'\\n', text, re.UNICODE)


def bot_send_message(message_chat_id, message, reply_markup=None):
    log.debug(implode_new_lines(message))
    bot.send_message(message_chat_id, message, reply_markup=reply_markup)


def get_miners_info(do_active=False):
    answer = ''
    new_hashrates = {}
    for miner in miners_settings:
        try:
            response = urllib2.urlopen('http://{}:{}/'.format(miners_settings[miner]['ip'], miners_settings[miner]['port']), timeout=3)
        except urllib2.URLError:
            status = 'Miner \'{}\' isn\'t running or freezed :(\n'.format(miner)
            if not do_active:
                answer += status
                continue
            else:
                status += 'Running \'miner_freezes_or_not_runnig\' script'
                log.warn(status)
                subprocess.call([settings['subprocess_windows_crutch'], miners_settings[miner]['miner_freezes_or_not_runnig']])
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
            format_dict['temp'] = format_dict['temp_fans'].split(';')[gpu_num * 2]
            format_dict['fan'] = format_dict['temp_fans'].split(';')[gpu_num * 2 + 1]
            gpu_order_no += 1
            answer += miners_settings[miner]['gpu_msg_format'].format(**format_dict)

        answer += miners_settings[miner]['postfix_msg_format'].format(**format_dict)
    if not do_active:
        return answer
    else:
        status = ''
        global previous_hasrates
        if settings['hashrate_fall_percentage'] > 0 and len(previous_hasrates) > 0:
            for miner in previous_hasrates:
                for i, previous_hasrate in enumerate(previous_hasrates[miner]):
                    if previous_hasrate > 0:
                        percent = 100.0 - float(new_hashrates[miner][i]) / previous_hasrate * 100
                        if percent >= miners_settings[miner]['hashrate_fall_percentage']:
                            status = ('Hashrate \'{}\'/{} lower by {:0.0f}%, running \'hashrate_falled\' script\n'
                                      'Previous info:\n{}' ).format(miner, i + 1, percent, answer)
                            log.warn(implode_new_lines(status))
                            break
                        subprocess.call([settings['subprocess_windows_crutch'], miners_settings[miner]['miner_freezes_or_not_runnig']])
        previous_hasrates = new_hashrates.copy()
        return status
