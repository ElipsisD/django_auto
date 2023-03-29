# django_auto

Сервис для контроля за уровнем цен на автомобильные запчасти на сайтах агрегаторов (на данный момент Autodoc.ru)

### Структура .env файла:

`AUTODOC_LOGIN`

`AUTODOC_PASSWORD`

`POSTGRES_DB`

`POSTGRES_USER`

`POSTGRES_PASSWORD`

`DB_HOST`

### План работ:

- парсинг сайта exist.ru с использованием selenium
- настройка celery beat
- создание API endpoint для работы с telegram ботом
- создание графика уровня цен на странице конкретной запчасти
