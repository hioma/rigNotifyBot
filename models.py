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
        storage = shelve.open(shelve_name)
        if not 'users' in storage:
            storage['users'] = {}
            logging.getLogger('bot').info('DB created')
        if telegram_nickname not in storage['users']:
            storage['users'][telegram_nickname] = {'chat_id': chat_id, 'active': True}
            logging.getLogger('bot').info('Added new user: @{} ({})'.format(telegram_nickname, chat_id))
        storage.close()
        return storage['users'][telegram_nickname]

    @staticmethod
    def get_active():
        storage = shelve.open(shelve_name)
        if 'users' in storage:
            for user in storage['users']:
                if storage['users'][user]['active']:
                    yield storage['users'][user]
        storage.close()
