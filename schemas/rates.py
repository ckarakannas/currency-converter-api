from ma import ma
from marshmallow import post_load, validate
from models.rates import RatesModel


class RatesSchema(ma.Schema):
    base = ma.Str(required=True)
    date = ma.Str()
    rates = ma.Dict(keys=ma.Str(validate=validate.Length(equal=3)), values=ma.Float(required=True), required=True)

    @post_load(pass_many=True)
    def create_rates_model(self, data, **kwargs):
        return RatesModel.create_dict(*data)


rates_schema = RatesSchema(many=True)
