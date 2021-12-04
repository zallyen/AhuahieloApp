from operator import add
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    telephone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer)
    productId = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    address = db.Column(db.String(1000))
    total = db.Column(db.Integer)
    date = db.Column(db.String(100))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    inventory = db.Column(db.Integer)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    telephone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date = db.Column(db.String(100))
    salary = db.Column(db.Integer)