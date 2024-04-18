from models.models import App


def create_app_for_db(kwargs):

    object_db = App(
        title=kwargs['title'],
        url=kwargs['url'],
        launch_url=kwargs['launch_url']
    )
    return object_db
