# -*- coding: utf-8 -*-

# Комментарии из файла "config_full.py" оставлены к тем значениям, которые вам, скорее всего, нужно будет поменять. Полее подробно написано в "config_full.py" и "README.md"

settings = {
    'bot_token': 'your_secret_telegram_token', # API-ключ вашего бота
    'allowed_users': ('your_telegram_nickname'), # список (регистрозависимый! без "@") пользователей, которым разрешёно пользование бота, если пустой - разрешено всем
    'passive_notification_timeout': 1*60*60,
    'active_notification_timeout': 60,
    'subprocess_windows_crutch': r'C:\Users\admin\Desktop\start_subprocess.bat', # костыль, путь к батнику, который будет запускать ваши батники, по-другому у меня не получилось реализовать запуск параллельного процесса в питоне. Образец лежит в папке "extas/"
    'system_reboot': r'C:\Users\admin\Desktop\kill_all_and_reboot.bat', # путь к батнику, который будет презапускать систему. Образец лежит в папке "extas/"
    'shelve_name': 'shelve.db',
}

miners_settings = {
    'miner: eth/dec': { # Имя можно поменять на удобное
        'ip': '127.0.0.1',
        'port': 3333,
        'di': '0123', # важный параметр! Определяет, какие карты используется майнером. Если он не задан в конфиге майнера, то пишите 01..N, где N - это количество ваших карт минус 1 (пример: '01234' для пяти карт, '01' - для двух). Если задан -- тогда сами знаете, что писать (как в майнере*)
                      # * до версии 9.7 майнера тут было 0345 для моего рига, теперь же eth-клеймор видит не все карты в системе, а только только те карты, которые были указаны в параметре -di.
                      # Короче, если майнером используются все карты в системе, то пишите '01..N', если это <9.5 eth-клеймор или <12.5 zec-клеймор, и используется часть карт, то -di параметр из start.bat, если >9.4 eth-клеймор, то 01..M, где M - это количество задействованных в майнере карт минус 1

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
        'computed_params': ('gpu_num', 'hashrate_primary', 'hashrate_secondary', 'temp', 'fan'),
        'divider': {'primary': 1000, 'secondary': 1000},
        'prefix_msg_format': '', # паттерн, который будет использован в сообщении от бота до блока с перечнем карт. Тут можно написать название майнера (например, 'Дуал eth/dec'), или общий хэшрейт ('Всего eth: {totalhashrate_primary}'), время работы ('Работает уже {workingtime} секунд') и прочие параметры, являющиеся общими для всех карт
        'gpu_msg_format': 'GPU{gpu_num}: {hashrate_primary:0.1f}mh/s ETH, {hashrate_secondary:0.0f}mhs DEC, {temp}°, {fan}% fan\n', # паттерн, из которого будет формироваться информация для каждой карты в отдельности. Пример: 'GPU{gpu_num}: {hashrate_primary:0.1f}mh/s ETH, {temp}°, {fan}% fan\n'. Используйте формат "variable_name:0.Nf" для редактирования количества знаков после запятой (N) для дробных чисел
        'postfix_msg_format': '', # паттерн, используемый после блоков gpu_msg_format, по аналогии с предыдущими блоками

        'miner_freezes_or_not_runnig': r'C:\Users\admin\Desktop\do_nothing.bat', # путь к батнику, который будет запускаться в случае, если бот не сможет подключиться к майнеру
        'hashrate_fall_percentage': 80, # определяет уровень падения хэшрейта майнера, при котором возникает событие "хэшрейт упал"
        'hashrate_falled': r'C:\Users\admin\Desktop\do_nothing.bat', # путь к батнику, который будет запускаться в случае, если на любой из карт майнера хэшрейт упал на "hashrate_fall_percentage" процентов
    }
}
