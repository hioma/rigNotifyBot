# rigNotifyBot

## Disclaimer ##
Я не профессиональный программист и даже не любитель, так что внутрь файлов лучше даже не заглядывать, бота писал под себя, но ввиду отсутствия альтернатив решил поделиться им с общественностью, авось кому-нибудь и пригодится.
Если есть какие-нибудь вопросы, обращайтесь в личку (на гитхабе она есть, да?), или на hioma[at]mail.ru, постараюсь помочь.

## Установка ##
* Установите [Python 2.7](https://www.python.org/downloads/release/python-2712/);
* Если будет отсутствовать PIP-установщик, то [скачайте](https://bootstrap.pypa.io/get-pip.py) `get-pip.py`, после запустите `python.exe get-pip.py`, после `pip install pyTelegramBotAPI`;
* Возьмите подходящий образец `config_*.py` из папки `config_examples`, переименуйте его в `config.py`, и положите рядом с `bot.py`;
* В своём телеграмм-аккаунте создайте бота через @botfather, получите токен, и пропишите его в файле `config.py`;
* Если при запуске (`python bot.py`) будут валиться ошибки "SNIMissingWarning" и "InsecurePlatformWarning", то выполните `pip install urllib3[secure]`;
