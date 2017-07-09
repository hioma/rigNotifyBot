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
и небольшая настройка bat'ников для удалённого запуска через PsExec.

## Установка ##
* Установите [Python 2.7](https://www.python.org/downloads/release/python-2712/);
* Если будет отсутствовать PIP-установщик, то [скачайте](https://bootstrap.pypa.io/get-pip.py) `get-pip.py`, после
запустите `python.exe get-pip.py`, после `pip install pyTelegramBotAPI`;
* Возьмите подходящий образец `config_*.py` из папки `config_examples`, переименуйте его в `config.py`, и положите
рядом с `bot.py`;
* В своём телеграмм-аккаунте создайте бота через @botfather, получите токен, и пропишите его в файле `config.py`;
* Скорее всего, при запуске (`python bot.py`) будут валиться ошибки "SNIMissingWarning" и "InsecurePlatformWarning",
поэтому выполните `pip install urllib3[secure]`;

## Настройка ##
Тут будут раскрыты параметры из `config.py`

## Советы ##
* При прописывании бота в автозапуск лучше назначить таймаут перед запуском (`TIMEOUT /T 60`), потому что бот может
инициализироваться первее майнеров и решить, что они не активны, и начать запускать заданные батники (среди которых
может быть ребут)
