# Комэксы Во Вконтаке

Данная программа может с помощью ВК Бота постить случайный комикс автора xkcd на стену группы

Для начала работы кода вам нужно создать файл `.env` с вашим `ID`  и `Access_token` `ом. <br> Файлик должен выглядеть примерно так:
```
CLIENT_ID=1337228
ACCESS_TOKEN=vk1.a.7unSSs4Mu982Hsaa_Po20ss0daIumPfEafsC4jQslMOOgYMHbIr9Q25byloekgE7yrwL3bB-bu2ka18VIIKa801Kvc9iif3ETOds_g
```
- `CLIENT_ID` - Вы сможете найти в **[Приложениях](https://dev.vk.com/ru)**, если быть точнее то во вкладке `Настройки` <br>
- `ACCESS_TOKEN` - Вы получите с помощью капошения в Адресной строке, надо будет просто подставить свои данные в **[уже готовую ссылку](https://dev.vk.com/ru/api/access-token/implicit-flow-user)** <br>
>**Не забудьте сахронить `.env`**

### Запуск!
-Надо установить зависимости из файла `requirements.txt` с помощью команды:
```
pip install -r requirements.txt
```
- Далее запускаем код с помощью команды `python main.py`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
