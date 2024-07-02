#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return "<h1> PLANTS API </h1>"

class Plants(Resource):
    def get (self):
        plants_dict = [plant.to_dict() for plant in Plant.query.all()]
        resp = make_response (jsonify(plants_dict),200)
        return resp
    
    def post (self):
        new_plant = Plant (
            name = request.json['name'],
            image = request.json.get('image'),
            price = request.json.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        
        new_plant_dict = new_plant.to_dict()
        resp = make_response(jsonify(new_plant_dict) , 201)
        return resp
    #pass

class PlantByID(Resource):
    def get (self, id):
        plant_dict = Plant.query.filter(Plant.id == id) .first().to_dict()
        return make_response (jsonify(plant_dict), 200)
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID,'/plants/<int:id>')    
    #pass
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
