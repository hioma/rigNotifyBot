# -*- coding: utf-8 -*-

import logging
import sys
import shelve
from config import shelve_name


reload(sys)
sys.setdefaultencoding('utf-8')


class Users:
    @staticmethod
    def get_or_create_user(telegram_nickname, chat_id):
        print 'here1'
        with shelve.open(shelve_name) as storage:
            print 'here2'
            if 'users' not in storage:
                storage['users'] = {}
                logging.getLogger('bot').info('DB created')
            print 'here3'
            if telegram_nickname not in storage['users']:
                storage['users'][telegram_nickname] = {'chat_id': chat_id, 'active': True}
                logging.getLogger('bot').info('Added new user: @{} ({})'.format(telegram_nickname, chat_id))
            return storage['users'][telegram_nickname]

    @staticmethod
    def get_active():
        with shelve.open(shelve_name) as storage:
            if 'users' in storage:
                for user in storage['users']:
                    if storage['users'][user]['active']:
                        yield storage['users'][user]
