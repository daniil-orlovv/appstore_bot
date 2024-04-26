# AppStoreBot

# Описание проекта
Telegram-бот, осуществляющий мониторинг доступности выбранных iOS приложений в App Store по URL и информирует пользователей о любых изменениях в их доступности.

Возможности администратора: 
- добавление приложений в бота, с указанием url, названия и ссылки для запуска(`/add`)
- удаление приложений из бота(`/remove`)
- установка интервала(`/setinterval`)
- генерация ключа доступа для пользователей(`/generatekey`)
- отправка сообщения всем пользователям бота(`/broadcast`)

Возможности пользователя:
- получение доступа к боту с помощью кода доступа, полученного у администратор(`/start`)
- получение статуса приложений, на обновления которых он подписан(`/status`)
- возможность подписки на приложения(`/subscribe`)
- получение ссылки для запуска приложения(`/getlaunchlinks`)

Возможности бота:
- бот периодически (интервал проверки задается администратором) отправляет запросы к страницам приложений в App Store. Приложение считается недоступным только после трех последовательных
неуспешных запросов, каждый успешный запрос сбрасывает счетчик неуспешных попыток на ноль
- в случае обнаружения недоступности приложения, бот отправляет уведомление всем подписанным пользователям о данном событии



# Установка, настройка и запуск проекта

### Запуск на компьютере
1. Сохранить проект в выбранную директорию: `git clone git@github.com:daniil-orlovv/appstore_bot.git`
2. Установить виртуальное окружение, находясь в корне проекта: `python -m venv venv`
3. Активировать виртуальное окружение: `source venv/scripts/activate`
4. Установить зависимости из файла requirements.txt: `pip install -r requirements.txt`
5. Создать файл .env и заполнить его по подобию .env.exapmle, указав:
   - BOT_TOKEN(можно получить в телеграм-боте `Bot Father`, создав своего бота)
   - INTERVAL_MINUTES(предварительная настройка интервала проверки доступа приложений в минутах)
   - ADMIN_IDS(Список админов приложения, необходимо указать свой TELEGRAM_ID или пользователя, которого нужно назначить админом)
6. Создать и выполнить миграции с помощью `alembic`:
   1. Перейти в корень и инициализировать `alembic`: `alembic init alembic`
   2. В файле alembic.ini указать путь до файла базы данных sqlite3: `sqlalchemy.url = sqlite:///sqlite3.db`
   3. По пути `alembic/` находим `env.py`и меняем строку `target_metadata = None` на:
      ```
      # Импорт вышестоящего каталога
      import os
      import sys
      sys.path.insert(0, '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))

      from myapp.mymodel import Base
      target_metadata = Base.metadata
      ```
      где `myapp.mymodel` путь до моделей БД -> `models.models`
   4. Создаем миграции: `alembic revision --message="Initial" --autogenerate`
   5. Применяем миграции: `alembic upgrade head`
7. Запускаем бота с помощью `python main.py`

   
# Использование: Подробные инструкции по использованию бота, включая доступные команды, функциональность и примеры взаимодействия с ним.

# Описание команд 

- `GET` -> `/api/v1/books` -> Получение всех книг
- `GET` -> `api/v1/book/{id}` -> Получение определенной книги по ее id
- `GET` -> `/api/v1/books?categories__title={Название категории}` -> Получение книг, отфильтрованных по опредеденной категории
- `GET` -> `/api/v1/books?title={Название книги}` -> Получение книг, отфильтрованных по названию
- `GET` -> `/api/v1/books?authors={Имя автора}` -> Получение книг, отфильтрованных по автору
- `GET` -> `/api/v1/books?status={Статус}` -> Получение книг, отфильтрованных по статусу
- `GET` -> `/api/v1/books?publisheddate={Дата публикации}` -> Получение книг, отфильтрованных по дате публикации

- `GET` -> `/api/v1/category` -> Получение всех категорий
- `GET` -> `/api/v1/subcategory/` -> Получение всех подктегорий

- `POST` -> `/api/v1/feedback/` -> Отправка обратной связи
Тело запроса:
{
    "email": "mail@mail.ru",
    "name": "Имя",
    "comment": "Коммент",
    "phone": "79999999999"
}

`POST` -> `/auth/users/` -> Создание(регистрация) юзера
Тело запроса:
```
{
    "username": "username",
    "password": "12345678abc"
}
```
Ответ:
```
{
    "email": "",
    "username": "username",
    "id": 2
}
```
- `POST` -> `/auth/jwt/create/` -> Получение токена для аутентификации
Тело запроса:
```
{
    "username": "username",
    "password": "12345678abc"
}
```
Ответ:
```
{
    "refresh": "eyJhbGciOiJIUzItNiIsInR5cCI6IrpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTE1MjUwNSwianRpIjoiMWIyN2U4OGYyZmM3NDViMzk5NzQzYjk4MGNiMjVjOTQiLCJ1c2VyX2lkIjoyfQ.jyj9E24EKF13UIZw9jGiDNKoFxbZ_mjXNcnf7HuaT6E",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMTUyNTA1LCJqdGkfOiJlN2RlM2NfWYxOTM0NGUwYTZjNzk1Nzk0MDJlNWRmOSIsInVzZXJfaWQiOjJ9.ANpkdo1L39o1x3QiYpVWRjUQuUNSc9MNnWJxObLULMQ"
}
```


Токен access использовать при запросе, указывая его в Authorization с типом `Bearer Token` без кавычек


- reDoc -> http://127.0.0.1:8000/redoc/
- Swagger -> http://127.0.0.1:8000/swagger/

Запросы тестировались с помощью `Postman`

# Стек технологий

- Django
- Django REST Framework
- Django Filter
- requests
- Djoser
- SimpeJWT
- Python-dotenv
- DRF-YASG
- SQLite
- Docker
- docker-compose
