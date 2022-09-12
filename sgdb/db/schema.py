from enum import Enum, unique

from sqlalchemy import (
    Column, MetaData, Table,
    Integer, Float, Boolean, String, DateTime, Enum as PgEnum, func
)


# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


@unique
class GameType(Enum):
    game = 'game'
    application = 'application'
    tool = 'tool'
    demo = 'demo'
    dlc = 'dlc'
    music = 'music'


games_table = Table(
    'games',
    metadata,

    Column('app_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('type', PgEnum(GameType, name='game_type')),
    Column('is_free', Boolean),
    Column('package_id', Integer),
    Column('has_trading_cards', Boolean),
    Column('price', Float),

    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now())
)
