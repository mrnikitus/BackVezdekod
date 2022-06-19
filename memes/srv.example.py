from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DEBUG = True # Режим отладки

ALLOWED_HOSTS = ['*'] # Разрешенные адреса

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1'] #Здесь тоже разрешенные адреса

SECRET_KEY = 'django-insecure-5$n&1)6j8ah%zlru2w$#pb^d)e0x1fgi#ea86u%n#v*t(53q47'
"""
Сгенерируйте новый ключ, если будете публиковать приложение (кроме тестовых запусков)
Выполните в командной строке в папке Django-проекта (`/memes/`) команду `python manage.py shell`
Далее следующие строчки:
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
Скопируйте получившийся ключ в поле выше
"""

# Настройка базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Если база данных MySQL, можно использовать следующую настройку.
# ЗАМЕНИТЕ имя_базы НА СВОЮ БАЗУ ДАННЫХ!
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': str(BASE_DIR / 'db.cnf'),
#             'charset': 'utf8mb4',
#             'init_command': 'ALTER DATABASE имя_базы CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci',
#         },
#     }
# }
