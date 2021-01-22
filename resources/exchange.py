from flask_restful import Resource, reqparse
from models.currency import CurrencyModel
from models.exchange import ExchangeModel


class Exchange(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('base_currency', type=str, required=True, help='Base currency type is required!')
    parser.add_argument('amount', type=float, required=True, help='Base amount to be converted is required!')
    parser.add_argument('target_currency', type=str, required=True, help='Target currency type is required!')

    def post(self):
        args = Exchange.parser.parse_args()
        base_currency = CurrencyModel(args['base_currency'], args['amount'])
        target_currency = ExchangeModel.convert(base_currency.amount, args['target_currency'])
        return {
            'target_currency': target_currency.currency,
            'converted_amount': target_currency.amount,
            'base_currency': base_currency.currency
        }
