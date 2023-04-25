# Тестовое задание на вакансию "Разработчик Python для написания автоматизаций и чат-ботов" ИП Богданов Денис александрович

Текст задания
https://disk.yandex.ru/i/9vcLnS28t9I7Dw

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```python
git clone https://github.com/sergeiivanitsa/multibot.git
```
```python
cd multibot
```
Cоздать и активировать виртуальное окружение:
```python
python3 -m venv venv
```
```python
source venv/bin/activate
```
Установить зависимости:
```python
pip install requirements
```
Создать файл .env в корневой папке проекта:
```python
touch .env
```
Указать константы
BOT_KEY = 'токен вашего бота (получить https://t.me/BotFather)'\n
WEATHER_API_KEY = 'Ваш API-ключ для доступа к OpenWeatherMap'
EX_API_KEY = 'Ваш API-ключ для доступа к Exchange Rates API'

Запустить проект
```python
python3 main.py
```
