from datetime import datetime, date
from itertools import product
import re
from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import login_required, current_user
from flask_login.utils import _get_user
from .models import *
from . import db
from flask.helpers import flash
from .access import requires_access_level

def producd(id):
    return Product.query.filter_by(id=id).first()

def userd(id):
    return User.query.filter_by(id=id).first()

admin = Blueprint('admin', __name__)

def product_bought(id):
    cap = 0
    bookings = Order.query.filter_by(productId=id).all()
    for i in bookings:
        cap += i.quantity
    return cap

@admin.route('/')
@requires_access_level('Administrador')
def dashboard():
    users = User.query.all()
    products = Product.query.all()
    employees = Employee.query.all()
    orders = Order.query.all()
    return render_template('dashboard.html', products=products, users=users, get_bought=product_bought, employees=employees, orders=orders, get_product=producd, get_user=userd)

@admin.route('/add-user', methods=['GET', 'POST'])
@requires_access_level('Administrador')
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        telephone = request.form.get('telephone')
        type = request.form.get('type')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('EL usuario ya existe')
            return redirect('/admin/add-user')
        else:
            new_user = User(email=email, name=name, password=password, address=address, telephone=telephone, type=type)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario creado!')

            """user = User.query.filter_by(email=email).first()
            login_user(user)"""

            return redirect(url_for('admin.dashboard'))
        
    return render_template('/add/user.html')

@admin.route('/add-product', methods=['GET', 'POST'])
@requires_access_level('Administrador')
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        inventory = request.form.get('inventory')
        
        user = Product(name=name, price=price, inventory=inventory)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('/add/product.html')

@admin.route('/add-employee', methods=['GET', 'POST'])
@requires_access_level('Administrador')
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        telephone = request.form.get('telephone')
        salary = request.form.get('salary')
        date = request.form.get('date')
        
        user = Employee(name=name, email=email, address=address, telephone=telephone, salary=salary, date=date)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('/add/employee.html')

@admin.route('/update-product/<int:id>', methods=['POST', 'GET'])
@requires_access_level('Administrador')
def update_product(id):
    if request.method == 'POST':
        updateProduct = Product.query.filter_by(id=id).first()
        name = request.form.get('name')
        price = request.form.get('price')
        inventory = request.form.get('inventory')

        product = Product(name=name,price=price,inventory=inventory)
        updateProduct.name = name
        updateProduct.price = price
        updateProduct.inventory = inventory
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    updateProduct = Product.query.filter_by(id=id).first()
    return render_template('/update/product.html', updateProduct=updateProduct)
    
@admin.route('/update-user/<int:id>', methods=['POST', 'GET'])
@requires_access_level('Administrador')
def update_user(id):
    if request.method == 'POST':
        updateUser = User.query.filter_by(id=id).first()
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        telephone = request.form.get('telephone')
        type = request.form.get('type')
        password = request.form.get('password')

        try:
            user = User(name=name,email=email,address=address,telephone=telephone,password=password,type=type)
            updateUser.name = name
            updateUser.email = email
            updateUser.address = address
            updateUser.telephone = telephone
            updateUser.type = type
            updateUser.password = password
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        except:
            flash('Ya existe un usuario con ese correo electronico')
            return redirect(url_for('admin.dashboard'))
    updateUser = User.query.filter_by(id=id).first()
    if updateUser.type == 'Administrador':
        oType = 'Normal'
    else:
        oType = 'Administrador'

    return render_template('/update/user.html', updateUser=updateUser, oType=oType)

@admin.route('/update-employee/<int:id>', methods=['POST', 'GET'])
@requires_access_level('Administrador')
def update_employee(id):
    if request.method == 'POST':
        updateEmployee = Employee.query.filter_by(id=id).first()
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('addresss')
        telephone = request.form.get('telephone')
        date = request.form.get('date')
        salary = request.form.get('salary')

        employee = Employee(name=name,email=email,address=address,telephone=telephone,date=date,salary=salary)
        updateEmployee.name = name
        updateEmployee.email = email
        updateEmployee.address = address
        updateEmployee.telephone = telephone
        updateEmployee.date = date
        updateEmployee.salary = salary
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    updateEmployee = Employee.query.filter_by(id=id).first()
    return render_template('/update/employee.html', updateEmployee=updateEmployee)

@admin.route('/update-order/<int:id>', methods=['POST', 'GET'])
@requires_access_level('Administrador')
def update_order(id):
    if request.method == 'POST':
        updateOrder = Order.query.filter_by(id=id).first()
        customerId = request.form.get('customerId')
        productId = request.form.get('productId')
        quantity = request.form.get('quantity')
        total = request.form.get('total')
        date = request.form.get('date')

        order = Order(customerId=customerId,productId=productId,quantity=quantity,date=date,total=total)
        updateOrder.customerId = customerId
        updateOrder.productId = productId
        updateOrder.quantity = quantity
        updateOrder.total = total
        updateOrder.date = date
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    updateOrder = Order.query.filter_by(id=id).first()
    users = User.query.all()
    products = Product.query.all()
    print(userd(2))
    return render_template('/update/order.html', updateOrder=updateOrder, users=users, products=products, get_product=producd, get_user=userd)

@admin.route('/delete-product/<int:id>', methods=['GET','POST'])
@requires_access_level('Administrador')
def delete_product(id):
    deleteProduct = Product.query.filter_by(id=id).first()
    if request.method == 'POST':
        if deleteProduct:
            db.session.delete(deleteProduct)
            db.session.commit()
            return redirect('/admin')

@admin.route('/delete-user/<int:id>', methods=['GET','POST'])
@requires_access_level('Administrador')
def delete_user(id):
    deleteUser = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        if deleteUser:
            db.session.delete(deleteUser)
            db.session.commit()
            return redirect('/admin')

@admin.route('/delete-employee/<int:id>', methods=['GET','POST'])
@requires_access_level('Administrador')
def delete_employee(id):
    deleteEmployee = Employee.query.filter_by(id=id).first()
    if request.method == 'POST':
        if deleteEmployee:
            db.session.delete(deleteEmployee)
            db.session.commit()
            return redirect('/admin')

@admin.route('/delete-order/<int:id>', methods=['GET','POST'])
@requires_access_level('Administrador')
def delete_order(id):
    deleteOrder = Order.query.filter_by(id=id).first()
    if request.method == 'POST':
        if deleteOrder:
            db.session.delete(deleteOrder)
            db.session.commit()
            return redirect('/admin')

"""@admin.route('/add-order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        date = request.form.get('date')
        total = request.form.get('total')
        
        user = Employee(name=name, email=email, address=address, telephone=telephone, salary=salary, date=date)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('/add/order.html')"""

