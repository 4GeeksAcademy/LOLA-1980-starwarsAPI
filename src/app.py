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
from models import db, User, Planets, People, FavoritePlanets
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

@app.route('/user', methods=['GET'])
def handle_hello():
    # SELECT * FROM 'user';
    # people query = Person.query.all()
    all_users = User.query.all()
    users_serialized = []
    for user in all_users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    #print(all_users[0].serialize())
    #print("tipo de dato", type(all_users[0].serialize()))
    return jsonify({ "data": users_serialized }), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    single_user = User.query.get(id)
    if single_user is None:
        return jsonify({"msg": "El usuario con el ID: {} no existe". format(id)}), 400
    #print(single_user)
    return jsonify({ "data": single_user.serialize() }), 200


@app.route('/planet', methods= ['GET'])
def get_planet():
    all_planets = Planets.query.all()
    planets_serialized = []
    for planet in all_planets:
        planets_serialized.append(planet.serialize())
        print(planets_serialized)
    return jsonify({ "data": planets_serialized }), 200


@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    single_planet = Planets.query.get(id)
    if single_planet is None:
        return jsonify({"msg": "El usuario con el ID: {} no existe". format(id)}), 400
    return jsonify({ "data": single_planet.serialize()}), 200


@app.route('/people', methods= ['GET'])
def get_people():
    all_people = People.query.all()
    people_serialized = []
    for people in all_people:
        people_serialized.append(people.serialize())
        print(people_serialized)
    return jsonify({ "data": people_serialized }), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_single_people(id):
    single_people = People.query.get(id)
    if single_people is None:
        return jsonify({"msg": "El personaje con el ID: {} no existe". format(id)}), 400
    return jsonify({ "data": single_people.serialize()}), 200


@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({ "msg": f"El usuario con ID {id} no exite"}), 404
    """
    favorite_planets= FavoritePlanets.query.filter_by(user_id=id).all()
    favorite_planets_serialized =[]
    for favorite_planet in favorite_planets:
        favorite_planets_serialized.append(favorite_planet.serialize())
    #print(favorite_planets)
    favorite_planets_serialized = list(map(lambda planet: planet.serialize(), favorite_planets))
    """
    favorite_planets = db. session.query(FavoritePlanets, Planets).\
        join(Planets).filter(FavoritePlanets.user_id==id).all()
    favorite_planets_serialized =[]
    for favorite_planet, planet in favorite_planets:
        favorite_planets_serialized.append({"favorite_planet_id": favorite_planet.id, "planet": planet.serialize()})
    print(favorite_planets)
    return jsonify({"msg": "OK", "favorite_planets": favorite_planets_serialized})


@app.route('/planet', methods=['POST'])
def new_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion al body"}), 400
    #obligatorios name y population
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatorio"}), 400
    if "population" not in body:
        return jsonify({"msg": "El campo population es obligatorio"}), 400
    
    new_planet = Planets()
    new_planet.name = body["name"]
    new_planet.population = body["population"] 
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Nuevo planeta creado",
                    "data": new_planet.serialize()}), 201


@app.route('/people', methods=['POST'])
def new_people():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar información en el body"}), 400
    # obligatorios name, height y mass
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatorio"}), 400
    if "height" not in body:
        return jsonify({"msg": "El campo height es obligatorio"}), 400
    if "mass" not in body:
        return jsonify({"msg": "El campo mass es obligatorio"}), 400
    
    new_person = People()
    new_person.name = body["name"]
    new_person.height = body["height"]
    new_person.mass = body["mass"]
    db.session.add(new_person)
    db.session.commit()

    return jsonify({"msg": "Nuevo personaje creado", "data": new_person.serialize()}), 201





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
