from ma import ma
from marshmallow import post_load, post_dump, EXCLUDE, validate
from models.exchange import ExchangeModel


class ExchangeSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
        dump_only = ("converted_amount", "conversion_rate", "description")
        ordered = True

    SKIP_VALUES = set([None])
    base = ma.Str(required=True, validate=validate.Length(equal=3))
    target = ma.Str(required=True, validate=validate.Length(equal=3))
    amount = ma.Float(required=True)
    converted_amount = ma.Float()
    conversion_rate = ma.Float()
    message = ma.Str()

    @post_load
    def create_exchange_model(self, data, **kwargs) -> "ExchangeModel":
        return ExchangeModel(**data)

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
        }
