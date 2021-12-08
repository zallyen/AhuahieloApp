from operator import add
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname1 = db.Column(db.String(100))
    lastname2 = db.Column(db.String(100))
    street = db.Column(db.String(100))
    number = db.Column(db.Integer)
    colony = db.Column(db.String(100))
    city = db.Column(db.String(100))
    codigoPostal = db.Column(db.Integer)
    password = db.Column(db.String(100))
    telephone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100))
    curp = db.Column(db.String(20), unique=True)
    rfc = db.Column(db.String(15), unique=True)
    state = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer)
    productId = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Integer)
    date = db.Column(db.String(100))
    date = db.Column(db.String(100))
    street = db.Column(db.String(100))
    number = db.Column(db.Integer)
    colony = db.Column(db.String(100))
    locality = db.Column(db.String(100))
    codigoPostal = db.Column(db.Integer)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    presentation = db.Column(db.String(100))
    price = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    inventory = db.Column(db.Integer)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname1 = db.Column(db.String(100))
    lastname2 = db.Column(db.String(100))
    street = db.Column(db.String(100))
    number = db.Column(db.Integer)
    colony = db.Column(db.String(100))
    city = db.Column(db.String(100))
    telephone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    nss = db.Column(db.Integer, unique=True)
    curp = db.Column(db.String(20), unique=True)
    codigoPostal = db.Column(db.Integer)

