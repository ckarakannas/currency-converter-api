from flask_restful import Resource
from flask import request
from schemas.rates import RatesSchema
from load_rates import rates_data

rates_schema = RatesSchema()
rates_list_schema = RatesSchema(many=True)


class SingleBaseRates(Resource):
    @classmethod
    def get(cls, base_currency: str):
        base_currency = base_currency.upper()
        query = rates_data.get(base_currency)
        if not query:
            return {"message": "Base currency {} is invalid or doesn't exist in database.".format(base_currency)}, 404
        return rates_schema.dump(query), 200

    @classmethod
    def post(cls, base_currency: str):
        base_currency = base_currency.upper()
        if rates_data.get(base_currency):
            return {"message": "Data for {} currency already exists!".format(base_currency)}, 409
        rates_json = request.get_json()
        rates_json['base'] = base_currency
        new_rates = rates_list_schema.load([rates_json])
        rates_data[base_currency] = new_rates[base_currency]
        return rates_schema.dump(new_rates[base_currency]), 201


class RatesList(Resource):
    @classmethod
    def get(cls):
        query = rates_data.values()
        if not query:
            return {"message": "Rates not found"}, 404
        return rates_list_schema.dump(query), 200
