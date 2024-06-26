lex_start = {
    'not_ket': 'Для доступа к боту необходимо указать ключ, который '
               'необходимо получить у администратора',
    'message': 'Доступ получен.',
    'else_message': 'Введен неверный ключ доступа! Обратитесь к '
                    'администратору.',
    'value_error': 'Необходимо указать ключ доступа через пробел '
                   'после команды:'
                   '\n\n<code>/start *значение*</code>',
    'logger_debug': 'Handler "start" has worked.'}

lex_status = {
    'ok_message': 'Доступные приложения:\n\n',
    'not_found_message': 'Недоступные приложения:\n\n',
    'logger_debug': 'Handler "status" has worked.'
}

lex_subscribe = {
    'message': 'На какое приложение нужно подписаться?',
    'else_message': 'Приложений для мониторинга нет.',
    'logger_debug': 'Handler "subscribe" has worked.'
}

lex_accept_subscribe = {
    'logger_debug': 'Handler "accept_subscribe" has worked.'
}

lex_get_launch_links = {
    'message': 'Для какого приложения получить ссылку для запуска?',
    'else_message': 'Приложений для мониторинга нет.',
    'logger_debug': 'Handler "get_launch_links" has worked.'
}

lex_accept_get_launch_links = {
    'message': 'Ссылка для запуска {title}: {url_app}',
    'logger_debug': 'Handler "accept_get_launch_links" has worked.'
}

lex_any_text = {
    'message': 'Пожалуйста, авторизуйтесь с помощью команды:\n\n /start *ключ*'
    '\n\nИли введите доступные команды:\n\n/status\n/subscribe\n'
    '/getlaunchlinks\n\nИли воспользуйтесь командой помощи:\n\n/help'
}

lex_help = {
    "message": 'Для авторизации в сервисе вам необходимо получить код доступа '
    'у админитратора @admin. После получения кода - ввести его вместе с '
    'командой:\n\n/start *ключ*\n\nДалее, вам станут доступны таки команды:'
    '\n\nКоманда /status - показывает статус приложений, на которые вы '
    'подписаны/\nКоманда /subscribe - создает подписку на приложения.\n'
    'Команда /getlaunchlinks - позволяет получить ссылку запуска для '
    'выбранного приложения'
}
