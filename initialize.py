#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import logging
import sys

import telebot

from config import *

reload(sys)
sys.setdefaultencoding('utf-8')

bot = telebot.TeleBot(settings['bot_token'])
last_start_time = None

logging_mode = logging.INFO
log = logging.getLogger('bot')
log.setLevel(logging_mode)
fh = logging.FileHandler('bot.log')
fh.setLevel(logging_mode)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(threadName)19s][%(module)12s][%(levelname)8s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)

q = Queue.Queue()
