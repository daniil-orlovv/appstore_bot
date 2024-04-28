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
- получение доступа к боту с помощью кода доступа, полученного у администратора(`/start`)
- получение статуса приложений, на обновления которых он подписан(`/status`)
- возможность подписки на приложения(`/subscribe`)
- получение ссылки для запуска приложения(`/getlaunchlinks`)

Возможности бота:
- бот периодически (интервал проверки задается администратором) отправляет запросы к страницам приложений в App Store. Приложение считается недоступным только после трех последовательных
неуспешных запросов, каждый успешный запрос сбрасывает счетчик неуспешных попыток на ноль
- в случае обнаружения недоступности приложения, бот отправляет уведомление всем подписанным пользователям о данном событии



# Установка, настройка и запуск проекта

### Запуск на компьютере
1. Сохраняем проект в выбранную директорию: `git clone https://github.com/daniil-orlovv/appstore_bot.git`
2. Устанавливаем виртуальное окружение, находясь в корне проекта: `python -m venv venv`
3. Активируем виртуальное окружение: `source venv/scripts/activate`
4. Устанавливаем зависимости из файла requirements.txt: `pip install -r requirements.txt`
5. Создаем файл .env и заполняем его по подобию .env.exapmle, указав:
   - BOT_TOKEN(можно получить в телеграм-боте `Bot Father`, создав своего бота)
   - INTERVAL_MINUTES(предварительная настройка интервала проверки доступа приложений в минутах)
   - ADMIN_IDS(Список админов приложения, необходимо указать свой TELEGRAM_ID или пользователя, которого нужно назначить админом)
6. Создаем и выполняем миграции с помощью `alembic`:
   - Переходим в корень и инициализируем `alembic`: `alembic init alembic`
   - В файле alembic.ini указываем путь до файла базы данных sqlite3: `sqlalchemy.url = sqlite:///sqlite3.db`
   - По пути `alembic/` находим `env.py`и меняем строку `target_metadata = None` на:
      ```
      # Импорт вышестоящего каталога
      import os
      import sys
      sys.path.insert(0, '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))

      from myapp.mymodel import Base
      target_metadata = Base.metadata
      ```
      где `myapp.mymodel` путь до моделей БД -> `models.models`
   - Создаем миграции: `alembic revision --message="Initial" --autogenerate`
   - Применяем миграции: `alembic upgrade head`
7. Запускаем бота с помощью `python main.py`

### Запуск на компьютере c помощью Docker
1. Сохраняем проект в выбранную директорию: `git clone https://github.com/daniil-orlovv/appstore_bot.git`
2. Создаем файл .env и заполняем его по подобию .env.exapmle, указав:
   - BOT_TOKEN(можно получить в телеграм-боте `Bot Father`, создав своего бота)
   - INTERVAL_MINUTES(предварительная настройка интервала проверки доступа приложений в минутах)
   - ADMIN_IDS(Список админов приложения, необходимо указать свой TELEGRAM_ID или пользователя, которого нужно назначить админом)
3. Создаем docker volume: `docker volume create sqlite_data`
4. Создаем образ: `docker build -t appstore_bot .`, находясь в корне проекта
5. Запускаем контейнер: `docker run --rm -it -p 8000:8000 --name appstore_bot -v sqlite_data:/data appstore_bot`

### Запуск на компьютере c помощью docker-compose
1. Сохраняем проект в выбранную директорию: `git clone https://github.com/daniil-orlovv/appstore_bot.git`
2. Создаем файл .env и заполняем его по подобию .env.exapmle, указав:
   - BOT_TOKEN(можно получить в телеграм-боте `Bot Father`, создав своего бота)
   - INTERVAL_MINUTES(предварительная настройка интервала проверки доступа приложений в минутах)
   - ADMIN_IDS(Список админов приложения, необходимо указать свой TELEGRAM_ID или пользователя, которого нужно назначить админом)
3. Создаем файл `sqlite3.db` в папке `data
4. Запускаем проект одной командой: `docker compose up`
      

### Запуск на сервере
1. Копируем проект с github на удаленный сервер: `git clone https://github.com/daniil-orlovv/appstore_bot.git`, находясь в домашней директории на сервере
2. Копируем файл .env с локальной машины: `scp /<путь_до_папки_с_файлом_.env>/.env mike@188.124.51.136:/home/mike/FSM_example_bot`
   Пример: `scp /Users/daniil/Desktop/Bots/appstore_bot/.env user@198.123.55.116:/home/user/appstore_bot`
3. Устанавливаем виртуальное окружение, находясь в корне проекта: `python3 -m venv venv`
4. Активируем виртуальное окружение: `source venv/bin/activate`
5. Устанавливаем необходимые зависимости: `pip install -r requirements.txt`
6. Запускаем бота: `python3 main.py`
   
**Для бесперебойной работы, при выключенном терминале:**
1. Переходим в директорию `cd /etc/systemd/system/`
2. Запускаем редактор: `sudo nano FSM_example_bot.service` или `nano FSM_example_bot.service`
3. Вставляем необходимые строки:
   ```
   [Unit]
   Description=appstore_bot
   After=syslog.target
   After=network.target
   
   [Service]
   Type=simple
   User=<имя_пользователя>
   WorkingDirectory=<путь_к_директории_с_ботом>
   ExecStart=<путь_к_интерпретатору_python_в_виртуальном_окружении> <путь_к_исполняемому_файлу_бота>
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
Пример файла:
   ```
   [Unit]
   Description=appstore_bot
   After=syslog.target
   After=network.target
   
   [Service]
   Type=simple
   User=daniil_orlovv
   WorkingDirectory=/home/daniil_orlovv/appstore_bot
   ExecStart=/home/daniil_orlovv/appstore_bot/venv/bin/python3 /home/daniil_orlovv/appstore_bot/main.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
4. Сохраняем файл, нажав следующую последовательность `CTRL + X` -> `y` -> `Enter`
5. Перезапускаем Systemd: `sudo systemctl daemon-reload`
6. Запускаем юнит: `sudo systemctl enable appstore_bot` -> `sudo systemctl start appstore_bot`
   
**Дополнительные возможности:**
- `sudo systemctl status appstore_bot` - проверка статуса юнита(выход: `:q`)
- `sudo systemctl restart appstore_bot` - перезапуск юнита
- `sudo systemctl stop appstore_bot` - остановка юнита
- `sudo systemctl disable appstore_bot` - отключение юнита
  
**Обновление бота:**
Из директории бота на сервере `cd /home/daniil_orlovv/appstore_bot` выполняем команду `git pull` и перезапускаем юнит: `sudo systemctl restart appstore_bot`

### Запуск на сервере с помощью docker-compose
1. Создаем на сервер папку проекта, например `appstore_bot`.
2. Создаем в папке файл `docker-compose.production.yml`
3. Заполняем файл:
   ```
   version: '3'

   volumes:
     sqlite:
   
   services:
     bot:
       image: daniilorlovv/appstore_bot
       env_file: .env
       volumes:
         - sqlite:/data/
   ```
   4. Копируем файл `.env` в папку с проектом на сервере с локальной машины или создаем новый:
      ```
      BOT_TOKEN='1082480872:AAHMmOo8SjnYM67Ikr2glRqXZEp6FZkFeLQ'
      INTERVAL_MINUTES='1'
      ADMIN_IDS='242043626'
      ```
   5. Запускаем проект с помощью команды: `docker compose -f docker-compose.production.yml up`

# Описание команд 
Администратор:
- `/add [урл приложения] [название приложения] [ссылка запуска]`: Администратор добавляет приложение с помощью этой команды, указывая обязательно через пробел урл, название и ссылку запуска. Все приложения сохраняются в БД.
- `/remove`: Администратор удаляет приложение. При нажатии на кнопку возвращается список кнопок с приложениями, при нажатии на которые, выбранное приложение удаляется.
- `/setinterval [значение в минутах]`: Администратор устанавливает интервал для проверки ботом доступности приложений, отправляю команду со значением в минутах, обязательно через пробел.
- `/generatekey [значение]`: Администратор генерирует код доступа для пользователей, отправляя команду вместе со значением кода, обязательно через пробел. Далее, сообщает код пользователю для его дальнейшей авторизации. После авторизации пользователя код автоматически удаляется.
- `broadcast [сообщение]`: Администратор с помощью этой команды отправляет сообщение всем пользователям бота, указав через пробел сообщение, которое нужно всем отправить.

Пользователь:
- `/start [код доступа]`: Пользователь активирует бота с помощью кода, полученного у администратора, обязательно через пробел после команды.
- `/subscribe`: Пользователь отправляет команду, в ответ ботом отправляется список приложений, на которые можно создать подписку. Пользователь выбирает приложение - создается подписка.
- `/status`: При отправке команды возвращаются статусы приложений, на которые подписан пользователь.
- `/getlaunchlinks`: Команда позволяет пользователю получить ссылки для запуска выбранных приложений. При отправке команды - бот отправляет список приложений. Пользователь выбирает приложение, в ответ приходит ссылка для запуска приложения.

Все команды для пользователя продублированы кнопками в телеграм-боте.

# Описание структуры проекта
- `config_data/config.py` - предназначен для хранения конфигов проекта, а именно токен бота, список админов, интервал проверки. Также, для загрузки конфигов при запуске и обновлении интервала проверки
- `data/`: директория для хранения БД
- `filters/`:
  - `filters.py` - фильтр для проверки приложения в БД
  - `permissions.py` - фильтры для проверки прав(Админ, Авторизованный)
- `handlers/`:
  - `admin_handlers.py` - обработчики, предназначенные для команд администратора
  - `user_handlers.py` - обработчики, предназначенные для команд пользователя
- `keyboards/keyboards_builder.py` - билдер для создания обычных и инлайн-клавиатур
- `lexicon/`:
  - `admin_handlers.py` - словарь для подстановки текста в обработчики команд админа
  - `user_handlers.py` - словарь для подстановки текста в обработчики команд пользователя
- `middlewares/middleware.py` - мидлварь, отвечающий за создание сессии БД перед фильтрами и передачу ее в обработчики
- `models/models.py` - модели БД
- `states/state.py` - состояния FSM
- `utils/`:
  - `utils_db.py` - утилиты(функции) для взаимодействия с БД
  - `utils.py` - утилиты(функции) для проверки доступности приложений
- `main.py` - точка входа в бота

# Стек технологий

- aiogram
- aiohttp
- SQLAlchemy
- alembic
- APScheduler
- environs
- python-dotenv
- logging
- docker
- docker-compose
- Ubuntu 22.04 LTS
- VPS
