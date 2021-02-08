from flask import Flask, jsonify
from flask_restful import Resource, Api
import config
from resources.exchange import Exchange, SingleBaseExchange, ExchangeMultiple
from resources.rates import SingleBaseRates, RatesList
from ma import ma
from marshmallow import ValidationError
from load_rates import rates_data

app = Flask(__name__)
app.config.from_object('config')
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello from the Currency Exchange API! Running on: {}".format(app.config['FLASK_ENV'].upper())}


api.add_resource(HelloWorld, '/')
api.add_resource(Exchange, '/exchange', )
api.add_resource(ExchangeMultiple, '/exchangeMany', )
api.add_resource(SingleBaseExchange, '/exchange/<string:base_currency>')
api.add_resource(SingleBaseRates, '/rates/<string:base_currency>')
api.add_resource(RatesList, '/ratesList')

if __name__ == '__main__':
    ma.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
