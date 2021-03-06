# rigNotifyBot

## Disclaimer ##
Я не профессиональный программист и даже не любитель, так что внутрь файлов лучше не заглядывать. Бота писал под себя,
но ввиду отсутствия альтернатив решил поделиться им с общественностью, может, кому-нибудь и пригодится. Необходимость
написания данного бота была обусловлена желанием мониторить/управлять ригом через Telegram-интерфейс, и отсутствие у
других решений возможности контролировать несколько майнеров, работающих на одной системе.

По коду -- я открыт для критики, но хотелось бы увидеть её в виде пул-реквеста :)

Если есть ещё какие-нибудь вопросы, обращайтесь в личку (на гитхабе она есть, да?), или на hioma[at]mail.ru, постараюсь
помочь.

## Концепция ##
На риг, работающий на ОС Windows (на Linux тоже должно работать, кроме запуска bat-файлов, но это решаемо) ставится
Python, в конфигурационных файлах прописываются параметры http-интерфейсов майнеров, по желанию задаются форматы
нотификаций, действия при падении хэшрейта или отваливании майнера, ну и прочие параметры, далее запускается бот -- и,
в принципе, всё.

Теоретически, бот может осуществлять мониторинг и управление майнерами, находящихся на других ригах, но для этого
требуется доступность для их http-интерфейсов (не проблема, если риги находятся в одной локальной сети или VPN),
и небольшая настройка батников для удалённого запуска через PsExec.

## Скриншоты ##
![image](https://user-images.githubusercontent.com/13254725/28004333-8a23d99c-654c-11e7-9d21-705b80ec76e1.png)
![image](https://user-images.githubusercontent.com/13254725/28004812-abb2f23e-654f-11e7-8607-86ef46ffbcfb.png)

## Установка ##
* Установите [Python 2.7](https://www.python.org/downloads/release/python-2712/);
* Для установки требуемых модулей необходим установщик PIP, у которого есть известные конфликты с не-латинскими именами
пользователей и компьютеров, т.е. с 99% в этом случае он работать не будет. Так что лучше заранее подготовиться и
создать пользователя с не-русским именем;
* Если будет отсутствовать PIP-установщик, то скачайте [(отсюда, например)](https://bootstrap.pypa.io/get-pip.py)
`get-pip.py`, после из cmd запустите `python.exe get-pip.py`, и затем `pip install pyTelegramBotAPI`;
* Возьмите подходящий образец `config_*.py` из папки `config_examples`, переименуйте его в `config.py`, подправьте под
себя, и положите рядом с `bot.py`;
* В своём телеграмм-аккаунте создайте бота через @botfather, получите токен, и пропишите его в файле `config.py`;
* Запускайте бота по команде `C:\Python27\python.exe bot.py`, или по примеру `extas/start_bot.bat`;
* Скорее всего, при запуске бота будут валиться warn'инги "SNIMissingWarning" и "InsecurePlatformWarning", чтобы они не
мешали, выполните `pip install urllib3[secure]`;

## Настройка ##
### Раздел settings ###
* bot_token - API-ключ вашего бота, раздаёт их @BotFather при создании оного;
* allowed_users - список (**регистрозависимый! без "@"**) пользователей, которым разрешёно пользование бота, если
пустой - разрешено всем. Задётся в формате ('user1', 'user2');
* passive_notification_timeout - таймаут в секундах, когда ботом будут отсылаться нотификации о состоянии дел, при этом
"активные" действия (запуски батников) осуществляться не будут;
* active_notification_timeout - таймаут в секундах, когда ботом будут проверяться параметры и производиться активные
дейстия (запустки батников);
* subprocess_windows_crutch - костыль, путь к батнику, который будет запускать ваши батники, по-другому у меня не
получилось реализовать запуск параллельного процесса в питоне. Образец лежит в папке "extas/";
* system_reboot - путь к батнику, который будет презапускать систему. Образец лежит в папке "extas/";
* shelve_name - путь к простой БД, хранящей информацию о пользователях бота. Параметр в настройке не нуждается.

### Раздел miners_settings ###
Данный раздел представляет из себя набор "майнеров" - блоков настроек http-интерфейсов и нотификаций для каждого
ПО-майнера. Например, у меня на риге запущено 2 майнера (eth и zec), каждый из которых видит одинаковый набор карт, но
майнит на разных, соответственно, у меня в разделе "miners_settings" прописано два "майнера" (пример -
"config_examples/config_full.py").
* ip - IP http-интерфейса майнера ('127.0.0.1', если майнер запущен на той же машине, что и бот);
* port - порт http-интерфейса майнера (для claymore's по-умолчанию - '3333');
* di - важный параметр! Определяет, какие карты используется майнером. Если он не задан в конфиге майнера, то пишите
01..N, где N - это количество ваших карт **минус 1** (пример: '01234' для **пяти** карт, '01' для **двух**).
Если задан -- тогда сами знаете, что писать (как в майнере, за исключением eth-клеймора версии старше 9.4);
* regex - строка для парсинга параметров из http-интерфейса майнера, для claymore's-майнеров в редактировании
не нуждается. Если хотите добавить поддержку других майнеров, то пишите в личку или на почту, будем думать;
* parsed_params - тут задаются имена переменных из http-интерфейса майнера, из которых потом можно сформировать
сообщение для нотификации в паттернах prefix_msg_format/gpu_msg_format/postfix_msg_format (расписаны ниже).
Например, майнер в http-интерфейсе отдаёт числа общего хэшрейта, или reject-шар как общих, так и каждой карты
в отдельности -- все эти вещи можно встроить в нотификации. В целом это поле в редактировании не нуждается;
* computed_params - переменные, которые вычисляются в коде бота. Упомянуты для справки и использования в блоке
паттернов "gpu_msg_format", в редактировании не нуждаются.
* divider - делитель для хэшрейта. Например, если майнер отдаёт значения в килохэшах, а вы хотите видеть мегахэши -
нужно задать "1000";
* prefix_msg_format - паттерн, который будет использован в сообщении от бота до блока с перечнем карт. Тут можно
написать название майнера (например, 'Дуал eth/dec'), или общий хэшрейт ('Всего eth: {totalhashrate_primary}'),
время работы ('Работает уже {workingtime} секунд') и прочие параметры, являющиеся общими для всех карт;
* gpu_msg_format - паттерн, из которого будет формироваться информация для каждой карты в отдельности. Пример:
'GPU{gpu_num}: {hashrate_primary:0.1f}mh/s ETH, {temp}°, {fan}% fan\n' (выдаст в стиле
'GPU2: 28.6mh/s ETH, 54°, 66% fan'). Используйте формат "variable_name:0.Nf" для задания количества знаков
после запятой (N) для дробных чисел;
* postfix_msg_format - паттерн, используемый после блоков gpu_msg_format, по аналогии с предыдущими блоками;
* miner_freezes_or_not_runnig - путь к батнику, который будет запускаться в случае, если бот не сможет подключиться к
майнеру;
* hashrate_fall_percentage - определяет уровень падения хэшрейта майнера, при котором возникает событие "хэшрейт упал";
* hashrate_falled - путь к батнику, который будет запускаться в случае, если на любой из карт майнера хэшрейт упал на
"hashrate_fall_percentage" процентов;


## Советы ##
* При прописывании бота в автозапуск лучше назначить таймаут перед запуском (`TIMEOUT /T 60`), потому что бот может
инициализироваться первее майнеров и решить, что они не активны, и начать запускать заданные батники (среди которых
может быть ребут);


## Донат ##
BTC: 16oNeHqWoqgvstvZhU93aYSM5aC9xmSmjs

ETH: 0xf6d7451B848986ef088F487E96e5892E71f124a8
