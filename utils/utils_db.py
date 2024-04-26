import logging

from sqlalchemy.orm import Session

from models.models import App, Key, User, UserApp

logger = logging.getLogger(__name__)


def create_app_obj_for_db(kwargs: dict) -> App:
    """Создает объект модели App для создания в БД."""

    logger.debug('func. create_app_obj_for_db has worked.')
    return App(title=kwargs['title'], url=kwargs['url'],
               launch_url=kwargs['launch_url'])


def create_user_app_obj_for_db(ids_users: int, ids_apps: list) -> UserApp:
    """Создает объект модели UserApp для создания в БД."""

    logger.debug('func. create_user_app_obj_for_db has worked.')
    return UserApp(user_id=ids_users[0], app_id=ids_apps[0])


def check_exist_app(session: Session, data: dict) -> bool:
    """Проверяет существование объекта в модели App по аргументам в БД."""

    title = data['title']
    url = data['url']
    launch_url = data['launch_url']
    check_name = session.query(App).filter(App.title == title).all()
    check_url = session.query(App).filter(App.url == url).all()
    check_launch_url = session.query(App).filter(App.title == launch_url).all()

    if check_name or check_url or check_launch_url:
        logger.debug('func. check_exist_app has worked -> False.')
        return False
    logger.debug('func. check_exist_app has worked -> True.')
    return True


def get_apps_from_db(session: Session) -> list[str]:
    """Получает имена приложений из модели App в БД."""

    apps = session.query(App.title).all()
    logger.debug('func. get_apps_from_db has worked')
    return [x[0] for x in apps]


def get_subscribing_apps_of_user(session: Session, user_id: int) -> dict:
    """Получает урлы приложений из модели App, на которые подписан
    пользователь."""

    id_user = session.query(User).filter(User.id_telegram == user_id).first()
    q_app = session.query(UserApp).filter(UserApp.user_id == id_user.id)
    ids_apps = [app.app_id for app in q_app]
    dict_urls = {}
    for id in ids_apps:
        url_app = session.query(App.url).filter(App.id == id).scalar()
        dict_urls[id] = url_app
    logger.debug('func. get_subscribing_apps_of_user has worked')
    return dict_urls


def create_subscribe_on_app(session: Session, title: str, user_id: int) -> str:
    """Создает подписку пользователя на приложение(Создает объект UserApp)."""

    q_app = session.query(App).filter(App.title == title)
    q_user = session.query(User).filter(User.id_telegram == user_id)
    ids_apps = [app.id for app in q_app]
    ids_users = [user.id for user in q_user]

    q_user_app = session.query(UserApp).filter(
        UserApp.app_id == ids_apps[0], UserApp.user_id == ids_users[0])

    if not q_user_app.first():
        obj_for_db = create_user_app_obj_for_db(ids_users, ids_apps)
        session.add(obj_for_db)
        session.commit()
        logger.debug('func. create_subscribe_on_app has worked')
        return 'Подписка оформлена!'
    logger.debug('func. create_subscribe_on_app has worked')
    return 'Вы уже подписаны на это приложение!'


def remove_app_from_db(session: Session, name_app: str) -> None:
    """Удаляет объект модели App из БД."""

    app = session.query(App).filter(App.title == name_app).one()
    session.delete(app)
    session.commit()
    logger.debug('func. remove_app_from_db has worked')


def add_app_to_db(session: Session, data: dict) -> None:
    """Добавляет объект модели App в БД."""

    object_for_db = create_app_obj_for_db(data)
    session.add(object_for_db)
    session.commit()
    logger.debug('func. add_app_to_db has worked')


def create_key_obj_for_db(key: str) -> Key:
    """Создает объект Key в БД."""

    logger.debug('func. create_key_obj_for_db has worked')
    return Key(title=key)


def check_exist_key(session: Session, data: dict) -> bool:
    """Проверяет существование объекта модели Key в БД по аргументам."""

    title = data
    check_key = session.query(Key).filter(Key.title == title).all()
    logger.debug('func. check_exist_key has worked')
    return False if check_key else True


def add_key_to_db(session: Session, key: str) -> None:
    """Добавляет объект модели Key."""

    object_for_db = create_key_obj_for_db(key)
    session.add(object_for_db)
    session.commit()
    logger.debug('func. add_key_to_db has worked')


def remove_key_from_db(session: Session, key: str) -> None:
    """Удаляет объект модели Key из БД."""

    key_for_deleting = session.query(Key).filter(Key.title == key).one()
    session.delete(key_for_deleting)
    session.commit()
    logger.debug('func. remove_key_from_db has worked')


def create_user_object_for_db(data: dict) -> User:
    """Создает объект модели User в БД."""

    logger.debug('func. create_user_object_for_db has worked')
    return User(id_telegram=data['id_telegram'], name=data['name'])


def check_exist_user(session: Session, id_telegram: int) -> bool:
    """Проверяет существование объекта модели User в БД."""

    users = session.query(User).filter(User.id_telegram == id_telegram).all()
    if users:
        logger.debug('func. check_exist_user has worked')
        return True
    logger.debug('func. check_exist_user has worked')
    return False


def add_user_to_db(session: Session, data: dict) -> None:
    """Добавляет объект модели User в БД."""

    object_for_db = create_user_object_for_db(data)
    session.add(object_for_db)
    session.commit()
    logger.debug('func. add_user_to_db has worked')


def get_ids_users_from_db(session: Session) -> list:
    """Получает id-s объектов из модели User."""

    q = session.query(User)
    logger.debug('func. get_ids_users_from_db has worked')
    return [user.id_telegram for user in q]


def check_user_in_db(session: Session, id_telegram: int):
    """Проверяет существование объекта модели User в БД."""

    logger.debug('func. check_access_for_user has worked')
    exist = session.query(User).filter(User.id_telegram == id_telegram).all()
    if not exist:
        return False
    return True


def check_access_for_user(session: Session, key: str) -> list[Key]:
    """Проверяет существование объекта модели Key в БД."""

    logger.debug('func. check_access_for_user has worked')
    return session.query(Key).filter(Key.title == key).all()


def return_launch_links(session: Session, title: str) -> str:
    """Возвращает ссылки запуска объекта модели App в БД."""

    logger.debug('func. return_launch_links has worked')
    return session.query(App.launch_url).filter(App.title == title).scalar()
