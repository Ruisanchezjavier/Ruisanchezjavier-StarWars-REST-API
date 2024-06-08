from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    home_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))
    favorites = db.Column(db.Integer, db.ForeignKey('favorite_people.id'))

    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "home_planet": self.home_planet,
            # do not serialize the password, its a security breach
        }
    
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250))
    homeworld_of = db.relationship('Person', backref='homeworld', lazy='dynamic')
    favorites = db.Column(db.Integer, db.ForeignKey('user_id_favorites.id'))
    
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            # do not serialize the password, its a security breach
        }
    
class Favorites_People(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id_favorites = db.Column(db.Integer, db.ForeignKey('users.id'))
     # favorite_of = db.relationship('Person', backref='favorite_people', lazy='dynamic')

     def serialize(self):
        return{
           "id": self.id,
           "user_id_favorites": self.user_id_favorites,
        }
    
class Favorites_Planets(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id_favorites = db.Column(db.Integer, db.ForeignKey('users.id'))
     # favorite_of = db.relationship('Planet', backref='favorite_planet', lazy='dynamic')

     def serialize(self):
        return{
           "id": self.id,
           "user_id_favorites": self.user_id_favorites,
        }
     


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorites_people_of = db.relationship('FavoritePeople', backref='user_id', lazy='dynamic')
    favorites_planets_of = db.relationship('FavoritePlanets', backref='user_id', lazy='dynamic')
    
    def __rep__(self):
        return '<user %r>' %self.username
    
    def serialize(self):
        return{
           "id": self.id,
           "name": self.name,
           "username": self.username,
        }