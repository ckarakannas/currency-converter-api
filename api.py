from flask import Flask
from flask_restful import Resource, Api
from resources.exchange import Exchange

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Exchange, '/exchange')

if __name__ == '__main__':
    app.run(debug=True)
