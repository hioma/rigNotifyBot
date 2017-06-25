#!/usr/bin/env python
# -*- coding: utf-8 -*-

from initialize import *
# import re
import os
# import time
from datetime import datetime
from telebot import types
# from models import User
# from threading import Thread
# from threads import queue_update_thread, notification_thread
from tools import implode_new_lines, bot_send_message


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
        bot_send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardHide())
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

        answer = 'Тут будет статистика:\n'
        bot_send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardHide())
    except Exception as e:
        log.error(
            '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                            sys.exc_info()[2].tb_lineno,
                                                            os.path.basename(
                                                                sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                            sys._getframe().f_code.co_name,
                                                            e))
