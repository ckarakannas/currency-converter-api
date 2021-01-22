from flask_restful import Resource, reqparse
from models.currency import CurrencyModel


class Currency(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('currency', type=str, required=True, help='Base type currency is required!')
    parser.add_argument('amount', type=float, required=True, help='Base amount to be converted is required!')

    def post(self):
        args = Currency.parser.parse_args()
        base_currency = CurrencyModel(args['currency'], args['amount'])
        return {'result': base_currency.json()}, 200