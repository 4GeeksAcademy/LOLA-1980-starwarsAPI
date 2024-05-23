from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'Usuario con email: {}'.format(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "password": self.password
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"Planet {self.id}: {self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population
        }


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"People {self.id}: {self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass
        }
    
class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.Integer, nullable=False)
    lenght = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Starship (self.id) (self.name) (self.model) (self.lenght)"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "lenght": self.lenght
        }
    
class FavoritePlanets(db.Model):
    __tablename__ = "favorite_planets"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user=db.relationship(User);
    planet_id=db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    planet=db.relationship(Planets)

    def __repr__(self):
        return f"al usuario {self.user_id} le gusta el planeta {self.planet_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
    

class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user=db.relationship(User);
    people_id=db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    people=db.relationship(People)

    def __repr__(self):
        return f"al usuario {self.user_id} le gusta el personaje {self.people_id}"
    
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }

