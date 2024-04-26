lex_add = {'message': 'Приложение {title} добавлено для мониторинга.',
           'else_message': 'Такое приложение уже существует!',
           'value_error': ('Необходимо указать url, название и ссылку для '
                           'запуска через пробел после команды: \n\n'
                           '<code>/add url title launch_url</code>'),
           'logger_debug': 'Handler "add" has worked.'}

lex_remove = {'message': 'Какое приложение необходимо удалить?',
              'else_message': 'Приложений для мониторинга нет.',
              'logger_debug': 'Handler "remove" has worked.'}

lex_accept_remove = {'message': 'Приложение {name_app} удалено!',
                     'logger_debug': 'Handler "accept_remove" has worked.'}

lex_set_interval = {'message': ('Интервал времени для проверки установлен: '
                                '{value} минут'),
                    'value_error': ('Необходимо указать значение интервала '
                                    'через пробел после команды в минутах:'
                                    '\n\n<code>/setinterval '
                                    '*значение*</code>'),
                    'logger_debug': 'Handler "set_interval" has worked.'}

lex_generate_key = {'message': 'Ключ доступа создан: {key_access}',
                    'else_message': 'Такой ключ уже существует!',
                    'value_error': ('Необходимо указать ключ доступа через '
                                    'пробел после команды:'
                                    '\n\n<code>/generatekey '
                                    '*значение*</code>'),
                    'logger_debug': 'Handler "generate_key" has worked.'}

lex_broadcast = {'value_error': ('Необходимо указать текст через пробел '
                                 'после команды:\n\n<code>/broadcast '
                                 '*значение*</code>'),
                 'logger_debug': 'Handler "broadcast" has worked.'}
