# -*- coding: utf-8 -*-

import re
from initialize import bot, log


def implode_new_lines(text):
    return re.sub(r'[\r\n]+', r'\\n', text, re.UNICODE)


def bot_send_message(message_chat_id, message, reply_markup=None):
    log.debug(implode_new_lines(message))
    bot.send_message(message_chat_id, message, reply_markup=reply_markup)
