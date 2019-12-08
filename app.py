import datetime

from flask import Flask
from flask_restful import Api, Resource
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields


app = Flask(__name__)
api = Api(app)

db = MongoEngine()
db.init_app(app)


class DataModel(db.Document):
    helmet_id = db.IntField(required=True)
    datetime = db.DateTimeField(default=datetime.datetime.utcnow)
    removal_sensor = db.BooleanField(required=True)
    collision_sensor = db.IntField(required=True)
    # air_quality_sensor = db.IntField(required=True)
    temperature_sensor = db.IntField(required=True)
    humidity_sensor = db.IntField(required=True)


class DataSchema(Schema):
    helmet_id = fields.Int(required=True)
    datetime = fields.DateTime(dump_only=True)
    removal_sensor = fields.Bool(required=True)
    collision_sensor = fields.Int(required=True)
    # air_quality_sensor = fields.Int(required=True)
    temperature_sensor = fields.Int(required=True)
    humidity_sensor = fields.Int(required=True)


class Ping(Resource):
    def post(self):
        return {'ping': 'pong'}


api.add_resource(Ping, '/ping')


if __name__ == '__main__':
    app.run(debug=True)
