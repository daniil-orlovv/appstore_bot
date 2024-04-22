from sqlalchemy import Engine

from models.models import App, Key, User, UserApp


def create_app_obj_for_db(kwargs: dict):

    object_db = App(
        title=kwargs['title'],
        url=kwargs['url'],
        launch_url=kwargs['launch_url']
    )
    return object_db


def create_user_app_obj_for_db(ids_users: int, ids_apps: list):

    object_db = UserApp(
       user_id=ids_users[0],
       app_id=ids_apps[0]
    )
    return object_db


def check_exist_app(session: Engine, data: dict) -> bool:
    title = data['title']
    url = data['url']
    launch_url = data['launch_url']
    check_name = session.query(App).filter(App.title == title).all()
    check_url = session.query(App).filter(App.url == url).all()
    check_launch_url = session.query(App).filter(App.title == launch_url).all()

    if check_name or check_url or check_launch_url:
        return False
    else:
        return True


def get_apps_from_db(session: Engine):
    apps = session.query(App.title).all()
    names_apps = [x[0] for x in apps]
    return names_apps


def get_subscribing_apps_of_user(session: Engine, user_id: int):

    id_user = session.query(User).filter(User.id_telegram == user_id).first()
    q_app = session.query(UserApp).filter(UserApp.user_id == id_user.id)
    ids_apps = [app.app_id for app in q_app]
    dict_urls = {}
    for id in ids_apps:
        url_app = session.query(App.url).filter(App.id == id).scalar()
        dict_urls[id] = url_app
    return dict_urls


def create_subscribe_on_app(session: Engine, title: str, user_id: int):

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
        return 'Подписка оформлена!'
    else:
        return 'Вы уже подписаны на это приложение!'


def remove_app_from_db(session: Engine, name_app: str):
    app = session.query(App).filter(App.title == name_app).one()
    session.delete(app)
    session.commit()


def add_app_to_db(session: Engine, data: dict):
    object_for_db = create_app_obj_for_db(data)
    session.add(object_for_db)
    session.commit()


def create_key_obj_for_db(key: str):

    object_db = Key(
        title=key
    )
    return object_db


def check_exist_key(session: Engine, data: dict):
    title = data
    check_key = session.query(Key).filter(Key.title == title).all()
    return False if check_key else True


def add_key_to_db(session: Engine, key: str):
    object_for_db = create_key_obj_for_db(key)
    session.add(object_for_db)
    session.commit()


def remove_key_from_db(session: Engine, key: str):
    key_for_deleting = session.query(Key).filter(Key.title == key).one()
    session.delete(key_for_deleting)
    session.commit()


def create_user_object_for_db(data: dict):
    object_db = User(
        id_telegram=data['id_telegram'],
        name=data['name']
    )
    return object_db


def check_exist_user(session: Engine, id_telegram: int):
    users = session.query(User).filter(User.id_telegram == id_telegram).all()
    if users:
        return True
    return False


def add_user_to_db(session: Engine, data: dict):
    object_for_db = create_user_object_for_db(data)
    session.add(object_for_db)
    session.commit()


def get_ids_users_from_db(session: Engine):
    q = session.query(User)
    ids_users = [user.id_telegram for user in q]
    return ids_users


def check_access_for_user(session: Engine, key: str):
    return session.query(Key).filter(Key.title == key).all()
