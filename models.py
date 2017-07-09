# -*- coding: utf-8 -*-

import logging
import shelve
import sys

from config import settings

reload(sys)
sys.setdefaultencoding('utf-8')


class Users:
    @staticmethod
    def get_or_create_user(telegram_nickname, chat_id):
        storage = shelve.open(settings['shelve_name'], writeback=True)
        if 'users' not in storage:
            storage['users'] = {}
            logging.getLogger('bot').info('DB created')
        if telegram_nickname not in storage['users']:
            storage['users'][telegram_nickname] = {'telegram_nickname': telegram_nickname, 'chat_id': chat_id,
                                                   'allowed': False, 'active': True}
            if len(settings['allowed_users']) == 0 or storage['users'][telegram_nickname]['telegram_nickname'] in \
                    settings['allowed_users']:
                storage['users'][telegram_nickname]['allowed'] = True

            logging.getLogger('bot').info('Added new user: @{} ({})'.format(telegram_nickname, chat_id))
        user = storage['users'][telegram_nickname]
        storage.close()
        return user

    @staticmethod
    def switch_user_status(telegram_nickname):
        storage = shelve.open(settings['shelve_name'], writeback=True)
        storage['users'][telegram_nickname]['active'] = not storage['users'][telegram_nickname]['active']
        storage.close()
        return storage['users'][telegram_nickname]

    @staticmethod
    def get_active():
        storage = shelve.open(settings['shelve_name'], writeback=True)
        if 'users' in storage:
            for user in storage['users']:
                if storage['users'][user]['active'] and storage['users'][user]['allowed']:
                    yield storage['users'][user]
        storage.close()
