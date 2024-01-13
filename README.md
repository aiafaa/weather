Как развернуть проект

Склонируйте проект командой: git clone https://github.com/aiafaa/weather.git

Создайте виртуальное окружение: python -m venv venv

Установите зависимости: pip install -r requirements.txt

Установите новый SECRET_KEY в файле core/settings.py, взять новый можно например - тут.

Создайте миграцию: python manage.py makemigrations python manage.py migrate

Создайте суперпользователя: python manage.py createsuperuser

Запустите проект командой - python manage.py runserver и перейдите в админку 127.0.0.1:8000/admin. В разделе WEATHER добавьте город, широту и долготу

Перейдите по ссылке 127.0.0.1:8000/weather?city=<citi_name>

<citi_name> - это название города на русском языке
