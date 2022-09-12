from http import HTTPStatus

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_response import Response
from aiohttp_apispec import docs, request_schema, response_schema
from sqlalchemy import and_

from sgdb.api.schema import GetGameResponseSchema, PatchGameSchema, PatchGameResponseSchema
from sgdb.db.schema import games_table

from .base import BaseGameView
from .query import GAMES_QUERY


class GameView(BaseGameView):
    URL_PATH = r'/games/{app_id:\d+}'

    @property
    def app_id(self):
        return int(self.request.match_info.get('app_id'))

    @staticmethod
    async def acquire_lock(conn, app_id):
        await conn.execute('SELECT pg_advisory_xact_lock($1)', app_id)

    @staticmethod
    async def get_game(conn, app_id):
        query = GAMES_QUERY.where(and_(
            games_table.c.app_id == app_id,
        ))
        return await conn.fetchrow(query)

    @classmethod
    async def update_game(cls, conn, app_id, data):
        values = {k: v for k, v in data.items()}
        if values:
            query = games_table.update().values(values).where(and_(
                games_table.c.app_id == app_id,
            ))
            await conn.execute(query)

    @docs(summary='Получить указанную игру')
    @response_schema(GetGameResponseSchema(), code=HTTPStatus.OK)
    async def get(self):
        async with self.pg.transaction() as conn:
            await self.acquire_lock(conn, self.app_id)

            game = await self.get_game(conn, self.app_id)
            if not game:
                raise HTTPNotFound()

        return Response(body={'data': game})

    @docs(summary='Обновить указанную игру')
    @request_schema(PatchGameSchema())
    @response_schema(PatchGameResponseSchema(), code=HTTPStatus.OK)
    async def patch(self):
        async with self.pg.transaction() as conn:
            await self.acquire_lock(conn, self.app_id)

            game = await self.get_game(conn, self.app_id)
            if not game:
                raise HTTPNotFound()

            await self.update_game(conn, self.app_id, self.request['data'])

            game = await self.get_game(conn, self.app_id)

        return Response(body={'data': game})
