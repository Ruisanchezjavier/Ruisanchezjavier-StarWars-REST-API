"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Person, Planet, Users, Favorite_Planets, Favorite_People

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# routes for people starwars

@app.route('/people', methods=['GET'])
def get_people():
    response_body = Person.query.all()
    response_body  = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_one_person(person_id):
    
    single_person = Person.query.get(person_id)
    if single_person is None:
        raise APIException(f"Person ID not found {person_id}", status_code=404)
    return jsonify(single_person.serialize()), 200


# routes for planet starwars

@app.route('/planets', methods=['GET'])
def get_planets():
    response_body = Planet.query.all()
    response_body  = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    
    single_planet = Planet.query.get(planet_id)
    if single_planet is None:
        raise APIException(f"Planet ID not found {planet_id}", status_code=404)
    return jsonify(single_planet.serialize()), 200


# users and favorites

@app.route('/users', methods=['GET'])
def get_all_users():
    response_body = Users.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_one_users(user_id):

    single_user = Users.query.get(user_id)
    if single_user is None:
        raise APIException(f"User ID not found {user_id}", status_code=404)
    return jsonify(single_user.serialize()), 200

@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def get_user_favorites(user_id):
    # Example to retrieve favorites of a user
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    favorites_people = user.favorites_people_of.all()
    favorites_planets = user.favorites_planets_of.all()

    serialized_people = [fav.serialize() for fav in favorites_people]
    serialized_planets = [fav.serialize() for fav in favorites_planets]

    return jsonify({
        "user": user.serialize(),
        "favorite_people": serialized_people,
        "favorite_planets": serialized_planets
    })
         
    

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_one_person_to_favorites():
    pass

@app.route('/users/<int:user_id>/favorite/planets/<int:planet_id>', methods=['POST'])
def add_one_planet_to_favorites():
    pass

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_one_person_from_favorites():
    pass

@app.route('/users/<int:user_id>/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_one_planet_from_favorites():
    pass











# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
