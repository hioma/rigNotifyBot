# -*- coding: utf-8 -*-

bot_token = 'your_secret_token'
shelve_name = 'shelve.db'

settings = {
    'passive_notification_timeout': 1*60*60,
    'active_notification_timeout': 60,
    'miner_freezes_or_not_runnig': r'C:\Users\admin\Desktop\do_nothing.bat',
    'hashrate_fall_percentage': 50,
    'hashrate_falled': r'C:\Users\admin\Desktop\do_nothing.bat',
}

miners = {
    'miner1: eth/dec': {
        'ip': '127.0.0.1',
        'port': 3333,
        'di': '012345', # если параметр -di не используется в майнере, то выставьте числа от 0 до (количество_карт - 1)
        'regex': r'\{"result": \["([^"]+?)", "([^"]+?)", "(\d+);(\d+);(\d+)", "([^"]+?)", "(\d+);(\d+);(\d+)", "([^"]+?)", "([^"]+?)", "([^"]+?)", "(\d+);(\d+);(\d+);(\d+)"',
        'parsed_params': ('miner_ver',
                        'workingtime',
                        'totalhashrate_primary', 'shares_primary', 'rejects_primary',
                        'hashrates_gpus_primary',
                        'totalhashrate_secondary', 'shares_secondary', 'rejects_secondary',
                        'hashrates_gpus_secondary',
                        'temp_fans',
                        'pools',
                        'invalid_shares_primary', 'pool_switches_primary', 'invalid_shares_secondary', 'pool_switches_secondary'),
        'computed_params': ('gpu_num', 'hashrate_primary', 'hashrate_secondary', 'temp', 'fan'), # для справки, отсюда значения не берутся, указаны для примера использования в gpu_msg_format
        'divider': {'primary': 1000, 'secondary': 1000},
        'prefix_msg_format': 'eth/dec:\n',
        'gpu_msg_format': 'GPU{gpu_num}: {hashrate_primary:0.1f}mh/s ETH, {hashrate_secondary:0.0f}mhs DEC, {temp}°, {fan}% fan\n',
        'postfix_msg_format': ''
    }
}
