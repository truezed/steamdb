from http import HTTPStatus

from aiohttp.web_response import Response
from aiohttp_apispec import docs, response_schema, request_schema

from sgdb.api.schema import GamesResponseSchema, GameSchema
from sgdb.utils.pg import SelectQuery

from .base import BaseGameView
from .query import GAMES_QUERY
from sgdb.db.schema import games_table


class GamesView(BaseGameView):
    URL_PATH = r'/games'

    @docs(summary='Отобразить все игры')
    @response_schema(GamesResponseSchema())
    async def get(self):
        query = GAMES_QUERY
        body = SelectQuery(query, self.pg.transaction())
        return Response(body=body)

    @docs(summary='Добавить игру')
    @request_schema(GameSchema())
    @response_schema(GamesResponseSchema(), code=HTTPStatus.CREATED)
    async def post(self):
        async with self.pg.transaction() as conn:
            query = games_table.insert().values(**self.request['data']).returning(games_table.c.app_id)
            app_id = await conn.fetchval(query)

        return Response(body={'data': {'app_id': app_id}}, status=HTTPStatus.CREATED)
