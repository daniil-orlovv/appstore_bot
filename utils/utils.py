import aiohttp
from sqlalchemy import Engine


from models.models import App


async def check_access_apps_subscribe(dict_urls: dict, session: Engine):
    apps_ok = {}
    apps_not_found = {}
    for id, url in dict_urls.items():
        async with aiohttp.ClientSession() as session_http:
            async with session_http.get(url) as resp:
                if resp.status == 200:
                    title_app = session.query(
                        App.title).filter(App.id == id).scalar()
                    apps_ok[title_app] = url
                else:
                    title_app = session.query(
                        App.title).filter(App.id == id).scalar()
                    apps_not_found[title_app] = url
    return apps_ok, apps_not_found
