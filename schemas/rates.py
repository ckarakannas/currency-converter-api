from ma import ma
from marshmallow import post_load, validate
from models.rates import RatesModel


class RatesSchema(ma.Schema):
    class Meta:
        ordered = True
    date = ma.Str()
    base = ma.Str(required=True, validate=validate.Length(equal=3))
    rates = ma.Dict(keys=ma.Str(validate=validate.Length(equal=3)), values=ma.Float(required=True), required=True)

    @post_load(pass_many=True)
    def create_rates_model(self, data, **kwargs):
        return RatesModel.create_dict(*data)


rates_list_schema = RatesSchema(many=True)
