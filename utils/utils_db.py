from sqlalchemy import Engine

from models.models import App, Key


def create_app_obj_for_db(kwargs: dict):

    object_db = App(
        title=kwargs['title'],
        url=kwargs['url'],
        launch_url=kwargs['launch_url']
    )
    return object_db


def add_app_to_db(session: Engine, data: dict):
    object_for_db = create_app_obj_for_db(data)
    session.add(object_for_db)
    session.commit()


def remove_from_db(session: Engine, name_app: str):
    app = session.query(App).filter(App.title == name_app).one()
    session.delete(app)
    session.commit()


def check_unique_app(session: Engine, data: dict) -> bool:
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


def check_key_access(session: Engine, data: str):
    title = data
    check_key = session.query(Key).filter(Key.title == title).all()
    return False if check_key else True


def create_key_obj_for_db(key: str):

    object_db = Key(
        title=key
    )
    return object_db


def add_key_to_db(session: Engine, key: str):
    object_for_db = create_key_obj_for_db(key)
    session.add(object_for_db)
    session.commit()
