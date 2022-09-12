from sqlalchemy import select

from sgdb.db.schema import games_table


GAMES_QUERY = select([
    games_table.c.app_id,
    games_table.c.name,
    games_table.c.type,
    games_table.c.is_free,
    games_table.c.package_id,
    games_table.c.has_trading_cards,
    games_table.c.price,
    games_table.c.created_at,
    games_table.c.updated_at,
])
