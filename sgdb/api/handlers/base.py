from aiohttp.web_urldispatcher import View
from asyncpgsa import PG


class BaseView(View):
    URL_PATH: str

    @property
    def pg(self) -> PG:
        return self.request.app['pg']


class BaseGameView(BaseView):
    @property
    def app_id(self):
        return int(self.request.match_info.get('app_id'))
