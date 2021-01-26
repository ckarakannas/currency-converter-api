from flask_restful import Resource
from flask import request
from schemas.exchange import ExchangeSchema
from load_rates import rates_data

exchange_schema = ExchangeSchema()
exchange_list_schema = ExchangeSchema(many=True)


def process_single_entry(exchange_json: dict):
    exchange = exchange_schema.load(exchange_json)
    currency_data = rates_data.get(exchange.base)
    if not currency_data:
        return {"message": "Base currency {0} does not exist in the database.".format(exchange.base)}, 400
    exchange.conversion_rate = currency_data.rates.get(exchange.target)
    if not exchange.conversion_rate:
        return {"message": "Target currency {0} does not exist in the database.".format(exchange.target)}, 400
    exchange.convert()
    return exchange_schema.dump(exchange), 201


def process_multiple_entries(exchange_json: dict):
    exchange = exchange_list_schema.load(exchange_json)
    for entry in exchange:
        currency_data = rates_data.get(entry.base)
        if not currency_data:
            entry.message = "Base currency {0} does not exist in the database.".format(entry.base)
            continue
        entry.conversion_rate = currency_data.rates.get(entry.target)
        if not entry.conversion_rate:
            entry.message = "Target currency {0} does not exist in the database.".format(entry.target)
            continue
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
        currency_data = rates_data.get(exchange.base)
        if not currency_data:
            return {"message": "Base currency {0} does not exist in the database.".format(exchange.base)}, 400
        exchange.conversion_rate = currency_data.rates.get(exchange.target)
        if not exchange.conversion_rate:
            return {"message": "Target currency {0} does not exist in the database.".format(
                exchange.target)}, 400
        exchange.convert()
        return exchange_schema.dump(exchange), 201
