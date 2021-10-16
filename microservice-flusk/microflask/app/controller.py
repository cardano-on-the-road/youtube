from flask import Flask
from flask import jsonify
import settings
from flask_restplus import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

lista = []



class posts(Resource):
    def get(self):
        print(lista)
        return lista, 200
    
    def post(self):
        p = api.payload
        print(type(p))
        lista.append(p)
        return api.payload, 201

    def put(self):
        pass

    def delete(self):
        pass

api.add_resource(posts, '/api/v1/posts/')


