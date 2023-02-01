from flask import Flask, json, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
app = Flask(__name__)
api = Api(app)


db = {
    "public_keys":{"PUa": None,
                   "PUb": None},
    "variables":{"g":None,
                 "prime_number_1":None,
                 "prime_number_2":None},
}

class Todo(Resource):
    def get(self, db_id, value):
        return db[db_id][value]

    def put(self, db_id, value):
        db[db_id][value] = request.form[value]

        return 201

api.add_resource(Todo, '/db/<db_id>/<value>')

if __name__ == '__main__':
    app.run(port=8000)
