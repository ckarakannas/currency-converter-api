from ma import ma
from marshmallow import pre_load, post_load, post_dump, EXCLUDE, validate, ValidationError
from models.exchange import ExchangeModel


class ExchangeSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
        dump_only = ("converted_amount", "conversion_rate", "description")
        ordered = True

    SKIP_VALUES = {None}
    base = ma.Str(required=True, validate=validate.Length(equal=3))
    target = ma.Str(required=True, validate=validate.Length(equal=3))
    amount = ma.Float(required=True)
    converted_amount = ma.Float()
    conversion_rate = ma.Float()
    message = ma.Str()

    @post_load
    def create_exchange_model(self, data, **kwargs) -> "ExchangeModel":
        data = self.format_currency_codes(data)
        return ExchangeModel(**data)

    def format_currency_codes(self, data):
        data['base'] = data['base'].upper()
        data['target'] = data['target'].upper()
        return data

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
        }
