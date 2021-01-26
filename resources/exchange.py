from flask_restful import Resource
from flask import request
from schemas.exchange import ExchangeSchema
from load_rates import rates_data

exchange_schema = ExchangeSchema()
exchange_list_schema = ExchangeSchema(many=True)


def process_single_entry(exchange_json: dict):
    exchange = exchange_schema.load(exchange_json)
    currency_data = rates_data.get(exchange.base.upper())
    if not currency_data:
        return {"message": "Base currency {0} does not exist in the database.".format(exchange.base.upper())}, 400
    conversion_rate = currency_data.rates.get(exchange.target.upper())
    if not conversion_rate:
        return {"message": "Target currency {0} does not exist in the database.".format(exchange.target.upper())}, 400
    exchange.conversion_rate = conversion_rate
    exchange.convert()
    return exchange_schema.dump(exchange), 201


def process_multiple_entries(exchange_json: dict):
    exchange = exchange_list_schema.load(exchange_json)
    for entry in exchange:
        currency_data = rates_data.get(entry.base.upper())
        if not currency_data:
            return {"message": "Base currency {0} does not exist in the database.".format(entry.base.upper())}, 400
        conversion_rate = currency_data.rates.get(entry.target.upper())
        if not conversion_rate:
            return {"message": "Target currency {0} does not exist in the database.".format(entry.target.upper())}, 400
        entry.conversion_rate = conversion_rate
        entry.convert()
    return exchange_list_schema.dump(exchange), 201


class Exchange(Resource):
    @classmethod
    def post(cls):
        exchange_json = request.get_json()
        return process_single_entry(exchange_json)


class ExchangeMultiple(Resource):
    @classmethod
    def post(cls):
        exchange_json = request.get_json()
        return process_multiple_entries(exchange_json)



class SingleBaseExchange(Resource):
    @classmethod
    def post(cls, base_currency: str):
        exchange_json = request.get_json()
        exchange_json["base"] = base_currency
        exchange = exchange_schema.load(exchange_json)
        currency_data = rates_data.get(exchange.base.upper())
        if not currency_data:
            return {"message": "Base currency provided does not exist in the database."}
        conversion_rate = currency_data.rates.get(exchange.target.upper())
        if not conversion_rate:
            return {"message": "Target currency provided does not exist in the database."}
        exchange.conversion_rate = conversion_rate
        exchange.convert()
        return exchange_schema.dump(exchange), 201
