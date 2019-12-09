import datetime

from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_mongoengine import MongoEngine
from marshmallow import Schema, fields, ValidationError


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


data_schema = DataSchema()


class DataList(Resource):
    def get(self):
        data = DataModel.objects()
        data = data_schema.dump(data, many=True)
        return data


class HelmetData(Resource):
    def get(self, helmet_id):
        data = DataModel.objects(helmet_id=helmet_id)

        if data.first() is None:
            abort(404, message="no data for helmet {}.".format(helmet_id))

        data = data_schema.dump(data, many=True)
        return data

    def post(self, helmet_id):
        json_input = request.get_json()
        json_input['helmet_id'] = helmet_id
        try:
            data = data_schema.load(json_input)
        except ValidationError as err:
            abort(422, errors=err.messages)

        data = DataModel(
            helmet_id=data['helmet_id'],
            removal_sensor=data['removal_sensor'],
            collision_sensor=data['collision_sensor'],
            temperature_sensor=data['temperature_sensor'],
            humidity_sensor=data['humidity_sensor'],
        )
        data.save()
        message = "Successfully created data for helmet {}.".format(
            data.helmet_id)

        data = data_schema.dump(data)
        data['message'] = message
        return data, 201

    def delete(self, helmet_id):
        data = DataModel.objects(helmet_id=helmet_id)
        if data.first() is None:
            abort(404, message="no data for helmet {}.".format(helmet_id))

        data.delete()
        return {"message": "helmet {} data deleted.".format(helmet_id)}


class LatestDataList(Resource):
    def get(self):
        data = DataModel.objects()
        helmet_ids = set(map(lambda d: d.helmet_id, data))

        data = []
        for helmet_id in helmet_ids:
            d = DataModel.objects(
                helmet_id=helmet_id
            ).order_by('-datetime').first()
            data.append(d)

        data = data_schema.dump(data, many=True)
        return data


class LatestHelmetData(Resource):
    def get(self, helmet_id):
        data = DataModel.objects(
            helmet_id=helmet_id
        ).order_by('-datetime').first()

        if data is None:
            abort(404, message="no data for helmet {}.".format(helmet_id))

        data = data_schema.dump(data)
        return data


class Ping(Resource):
    def post(self):
        return {'ping': 'pong'}


api.add_resource(Ping, '/ping')
api.add_resource(DataList, '/data')
api.add_resource(HelmetData, '/data/<string:helmet_id>')
api.add_resource(LatestDataList, '/latest-data')
api.add_resource(LatestHelmetData, '/latest-data/<string:helmet_id>')


if __name__ == '__main__':
    app.run(debug=True)
