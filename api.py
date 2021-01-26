from flask import Flask, jsonify
from flask_restful import Resource, Api
from resources.exchange import Exchange, SingleBaseExchange, ExchangeMultiple
from ma import ma
from marshmallow import ValidationError
from load_rates import rates_data

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


class HelloWorld(Resource):
    def get(self):
        return {'Hello from the Currency Exchange API!'}


api.add_resource(HelloWorld, '/')
api.add_resource(Exchange, '/exchange', )
api.add_resource(ExchangeMultiple, '/exchangeMany', )
api.add_resource(SingleBaseExchange, '/exchange/<string:base_currency>')

if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5000, debug=True)
