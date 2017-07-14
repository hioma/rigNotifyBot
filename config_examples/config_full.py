# -*- coding: utf-8 -*-

# Ознакомительный конфиг, в котором расписан сложный случай двух майнеров на одном риге и описан каждый параметр.
# Если у вас в системе стоит один майнер, то возьмите файлы "config_claymore_eth.py" или "config_claymore_zec.py",
# и переделайте их под себя.

settings = {
    'bot_token': 'your_secret_telegram_token', # API-ключ вашего бота
    'allowed_users': ('your_telegram_nickname'), # список (регистрозависимый! без "@") пользователей, которым разрешёно пользование бота, если пустой - разрешено всем. Задётся в формате ('user1', 'user2')
    'passive_notification_timeout': 1*60*60, # таймаут в секундах (1*60*60=3600, столько секунд в одном часе), когда ботом будут отсылаться нотификации о состоянии дел, при этом "активные" действия (запуски батников) осуществляться не будут
    'active_notification_timeout': 60, # таймаут в секундах, когда ботом будут проверяться параметры и производиться активные дейстия (запустки батников)
    'subprocess_windows_crutch': r'C:\Users\admin\Desktop\start_subprocess.bat', # костыль, путь к батнику, который будет запускать ваши батники, по-другому у меня не получилось реализовать запуск параллельного процесса в питоне. Образец лежит в папке "extas/"
    'system_reboot': r'C:\Users\admin\Desktop\kill_all_and_reboot.bat', # путь к батнику, который будет презапускать систему. Образец лежит в папке "extas/"
    'shelve_name': 'shelve.db', # путь к простой БД, хранящей информацию о пользователях бота. Параметр в настройке не нуждается
}

miners_settings = {
    'miner1: eth/dec': { # первый майнер, ETH
        'ip': '127.0.0.1', # IP http-интерфейса майнера
        'port': 3333, # порт http-интерфейса майнера
        'di': '0123', # важный параметр! Определяет, какие карты используется майнером. Если он не задан в конфиге майнера, то пишите 01..N, где N - это количество ваших карт минус 1 (пример: '01234' для пяти карт, '01' - для двух). Если задан -- тогда сами знаете, что писать (как в майнере*)
                      # * до версии 9.7 майнера тут было 0345 для моего рига, теперь же eth-клеймор видит не все карты в системе, а только только те карты, которые были указаны в параметре -di.
                      # Короче, если майнером используются все карты в системе, то пишите '01..N', если это <9.5 eth-клеймор или <12.5 zec-клеймор, и используется часть карт, то -di параметр из start.bat, если >9.4 eth-клеймор, то 01..M, где M - это количество задействованных в майнере карт минус 1

        'regex': r'\{"result": \["([^"]+?)", "([^"]+?)", "(\d+);(\d+);(\d+)", "([^"]+?)", "(\d+);(\d+);(\d+)", "([^"]+?)", "([^"]+?)", "([^"]+?)", "(\d+);(\d+);(\d+);(\d+)"', # строка для парсинга параметров из http-интерфейса майнера
        'parsed_params': ('miner_ver', # перечень распарсенных имена переменных из http-интерфейса, для использования в паттернах нотификаций в блоках prefix_msg_format/gpu_msg_format/postfix_msg_format. В редактировании не нуждается
                          'workingtime',
                          'totalhashrate_primary', 'shares_primary', 'rejects_primary',
                          'hashrates_gpus_primary',
                          'totalhashrate_secondary', 'shares_secondary', 'rejects_secondary',
                          'hashrates_gpus_secondary',
                          'temp_fans',
                          'pools',
                          'invalid_shares_primary', 'pool_switches_primary', 'invalid_shares_secondary', 'pool_switches_secondary'),
        'computed_params': ('gpu_num', 'hashrate_primary', 'hashrate_secondary', 'temp', 'fan'), # переменные, которые вычисляются в коде бота. Упомянуты для справки и использования в блоке паттернов "gpu_msg_format", в редактировании не нуждаются
        'divider': {'primary': 1000, 'secondary': 1000}, # делитель для хэшрейта. Например, если майнер отдаёт значения в килохэшах, а вы хотите видеть мегахэши - нужно задать "1000"
        'prefix_msg_format': 'eth/dec:\n', # паттерн, который будет использован в сообщении от бота до блока с перечнем карт. Тут можно написать название майнера (например, 'Дуал eth/dec'), или общий хэшрейт ('Всего eth: {totalhashrate_primary}'), время работы ('Работает уже {workingtime} секунд') и прочие параметры, являющиеся общими для всех карт
        'gpu_msg_format': 'GPU{gpu_num}: {hashrate_primary:0.1f}mh/s ETH, {hashrate_secondary:0.0f}mhs DEC, {temp}°, {fan}% fan\n', # паттерн, из которого будет формироваться информация для каждой карты в отдельности. Пример для соло-майнинга (без хэшрейта дуала): 'GPU{gpu_num}: {hashrate_primary:0.1f}mh/s ETH, {temp}°, {fan}% fan\n'. Используйте формат "variable_name:0.Nf" для редактирования количества знаков после запятой (N) для дробных чисел
        'postfix_msg_format': '', # паттерн, используемый после блоков gpu_msg_format, по аналогии с предыдущими блоками

        'miner_freezes_or_not_runnig': r'C:\Users\admin\Desktop\do_nothing.bat', # путь к батнику, который будет запускаться в случае, если бот не сможет подключиться к майнеру
        'hashrate_fall_percentage': 80, # определяет уровень падения хэшрейта майнера, при котором возникает событие "хэшрейт упал"
        'hashrate_falled': r'C:\Users\admin\Desktop\do_nothing.bat', # путь к батнику, который будет запускаться в случае, если на любой из карт майнера хэшрейт упал на "hashrate_fall_percentage" процентов
        'timeout': 3, # таймаут подключения к http-интерфейсу майнера. Если у вас сильно тормозит система, но при этом успешно майнит, то можно поднять таймаут до нужного числа секунд
    },
    'miner2: zec': { # Второй майнер, ZEC, все параметры идентичны описанным
        'ip': '127.0.0.1',
        'port': 3334,
        'di': '23',

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
        'divider': {'primary': 1, 'secondary': 1},
        'prefix_msg_format': 'zec:\n',
        'gpu_msg_format': 'GPU{gpu_num}: {hashrate_primary:0.0f}sol/s ZEC, {temp}°, {fan}% fan\n',
        'postfix_msg_format': '',

        'miner_freezes_or_not_runnig': r'C:\Users\admin\Desktop\do_nothing.bat',
        'hashrate_fall_percentage': 80,
        'hashrate_falled': r'C:\Users\admin\Desktop\do_nothing.bat',
    }
}
