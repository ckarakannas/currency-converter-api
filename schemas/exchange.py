from ma import ma
from marshmallow import post_load, EXCLUDE, validate
from models.exchange import ExchangeModel


class ExchangeSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
        dump_only = ("converted_amount", "conversion_rate")
        ordered = True
    base = ma.Str(required=True, validate=validate.Length(equal=3))
    target = ma.Str(required=True, validate=validate.Length(equal=3))
    amount = ma.Float(required=True)
    converted_amount = ma.Float()
    conversion_rate = ma.Float()
    description = ma.Str()

    @post_load
    def create_exchange_model(self, data, **kwargs) -> "ExchangeModel":
        return ExchangeModel(**data)