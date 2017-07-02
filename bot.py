#!/usr/bin/env python
# -*- coding: utf-8 -*-

from initialize import *
import os
import time
from datetime import datetime
from threading import Thread
from threads import passive_notification_queue_update_thread, notifications_send_thread, \
    active_notification_queue_update_thread
from tools import implode_new_lines, bot_send_message, get_miners_info
from models import Users


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


def get_user_info_and_check_timestamp(message):
    try:
        if request_is_old(message):
            return False

        user = Users.get_or_create_user(message.chat.username, message.chat.id)
        return user
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
        user = get_user_info_and_check_timestamp(message)
        if not user:
            return False

        info = get_miners_info()
        bot_send_message(message.chat.id, info)
    except Exception as e:
        log.error(
            '! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
                                                            sys.exc_info()[2].tb_lineno,
                                                            os.path.basename(
                                                                sys.exc_info()[2].tb_frame.f_code.co_filename),
                                                            sys._getframe().f_code.co_name,
                                                            e))


if __name__ == '__main__':
    queue_thread1 = queue_thread2 = notification_threads_array = None
    while True:
        try:
            last_start_time = datetime.now()
            log.info('starting bot in {}'.format(last_start_time))

            if queue_thread1 is None:
                queue_thread1 = Thread(target=passive_notification_queue_update_thread, name='QueueThread')
                queue_thread1.daemon = True
                queue_thread1.start()

            if queue_thread2 is None:
                queue_thread2 = Thread(target=active_notification_queue_update_thread, name='QueueThread')
                queue_thread2.daemon = True
                queue_thread2.start()

            if notification_threads_array is None:
                notification_threads_array = []
                for i in range(1):
                    notification_threads_array.append(
                        Thread(target=notifications_send_thread, name='NotificationThread{}'.format(i)))
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
