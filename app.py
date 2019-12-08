from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class Ping(Resource):
    def post(self):
        return {'ping': 'pong'}


api.add_resource(Ping, '/ping')


if __name__ == '__main__':
    app.run(debug=True)
