from marshmallow import Schema
from marshmallow.fields import Float, Int, Bool, Str, Nested
from marshmallow.validate import Length, OneOf, Range

from sgdb.db.schema import GameType


class GameSchema(Schema):
    app_id = Int(validate=Range(min=1), strict=True)
    name = Str(validate=Length(min=1, max=256))
    type = Str(validate=OneOf([type.value for type in GameType]))
    is_free = Bool()
    package_id = Int(validate=Range(min=1), strict=True)
    has_trading_cards = Bool()
    price = Float(validate=Range(min=0))


class PatchGameSchema(GameSchema):
    name = Str(validate=Length(min=1, max=256))
    type = Str(validate=OneOf([type.value for type in GameType]))
    is_free = Bool()
    package_id = Int(validate=Range(min=1), strict=True)
    has_trading_cards = Bool()
    price = Float(validate=Range(min=0))


class GamesResponseSchema(Schema):
    data = Nested(GameSchema(many=True), required=True)


class GetGameResponseSchema(Schema):
    data = Nested(GameSchema(), required=True)


class PatchGameResponseSchema(Schema):
    data = Nested(GameSchema(), required=True)
