# Как развернуть проект

1. Склонируйте проект командой: git clone https://github.com/aiafaa/weather.git

2. Создайте виртуальное окружение: `python -m venv venv`

3. Активируйте окружение: `venv/Scripts/activate` (venv/bin/activate для Linux)

4. Установите зависимости: `pip install -r requirements.txt`

5. Установите новый SECRET_KEY в файле core/settings.py, взять новый можно например - [тут](djecrety.ir).

6. Создайте миграцию: `python manage.py makemigrations` `python manage.py migrate`

7. Создайте суперпользователя: `python manage.py createsuperuser`

8. Запустите проект командой - `python manage.py runserver` и перейдите в админку 127.0.0.1:8000/admin. В разделе WEATHER добавьте город, широту и долготу

9. Перейдите по ссылке 127.0.0.1:8000/weather?city=<citi_name>

<citi_name> - это название города на русском языке
