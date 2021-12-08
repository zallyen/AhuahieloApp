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
from sqlalchemy import desc

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
    users = User.query.order_by(User.name)
    products = Product.query.order_by(Product.presentation)
    employees = Employee.query.order_by(Employee.name)
    orders = Order.query.all()
    return render_template('dashboard.html', products=products, users=users, get_bought=product_bought, employees=employees, orders=orders, get_product=producd, get_user=userd)

@admin.route('/add-user', methods=['GET', 'POST'])
@requires_access_level('Administrador')
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname1 = request.form.get('lastname1')
        lastname2 = request.form.get('lastname2')
        email = request.form.get('email')
        street = request.form.get('street')
        number = request.form.get('number')
        colony = request.form.get('colony')
        city = request.form.get('city')
        codigoPostal = request.form.get('codigoPostal')
        telephone = request.form.get('telephone')
        type = request.form.get('type')
        curp = request.form.get('curp')
        rfc = request.form.get('rfc')
        state = request.form.get('state')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        user1 = User.query.filter_by(curp=curp).first()
        user2 = User.query.filter_by(rfc=rfc).first()
        if user or user1 or user2:
            flash('Error: algunos datos que ingreso pertenecen a otro usuario')
        else:
            new_user = User(email=email, name=name, password=password, 
            street=street, number=number, colony =colony, city=city, telephone=telephone,
            type=type, lastname1=lastname1, lastname2=lastname2, codigoPostal=codigoPostal
            , curp=curp, rfc=rfc, state=state)
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
        presentation = request.form.get('presentation')
        weight = request.form.get('weight')
        price = request.form.get('price')
        inventory = request.form.get('inventory')
        
        user = Product(presentation=presentation, weight=weight, price=price, inventory=inventory)
        db.session.add(user)
        db.session.commit()
        flash('Producto creado')
        return redirect(url_for('admin.dashboard'))

    return render_template('/add/product.html')

@admin.route('/add-employee', methods=['GET', 'POST'])
@requires_access_level('Administrador')
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname1 = request.form.get('lastname1')
        lastname2 = request.form.get('lastname2')
        curp = request.form.get('curp')
        nss = request.form.get('nss')
        street = request.form.get('street')
        number = request.form.get('number')
        colony = request.form.get('colony')
        city = request.form.get('city')
        codigoPostal = request.form.get('codigoPostal')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        salary = request.form.get('salary')
        date = request.form.get('date')

        employee1 = Employee.query.filter_by(email=email).first()
        employee2 = Employee.query.filter_by(curp=curp).first()
        employee3 = Employee.query.filter_by(nss=nss).first()
        if employee1 or employee2 or employee3:
            flash("Error: algunos datos que ingreso pertenecen a otro empleado")
        else:
            employee = Employee(name=name, email=email, lastname1=lastname1, lastname2=lastname2, curp=curp, nss=nss, street=street, number=number, colony=colony, city=city, codigoPostal=codigoPostal, telephone=telephone, salary=salary, date=date)
            db.session.add(employee)
            db.session.commit()
            flash('Empleado creado')
            return redirect(url_for('admin.dashboard'))

    return render_template('/add/employee.html')

@admin.route('/update-product/<int:id>', methods=['POST', 'GET'])
@requires_access_level('Administrador')
def update_product(id):
    if request.method == 'POST':
        updateProduct = Product.query.filter_by(id=id).first()
        presentation = request.form.get('presentation')
        weight = request.form.get('weight')
        price = request.form.get('price')
        inventory = request.form.get('inventory')

        product = Product(presentation=presentation, weight=weight, price=price,inventory=inventory)
        updateProduct.presentation = presentation
        updateProduct.weight = weight
        updateProduct.price = price
        updateProduct.inventory = inventory
        db.session.commit()
        flash('Producto actualizado correctamente')
        return redirect(url_for('admin.dashboard'))
    updateProduct = Product.query.filter_by(id=id).first()
    return render_template('/update/product.html', updateProduct=updateProduct)
    
@admin.route('/update-user/<int:id>', methods=['POST', 'GET'])
@requires_access_level('Administrador')
def update_user(id):
    if request.method == 'POST':
        updateUser = User.query.filter_by(id=id).first()
        name = request.form.get('name')
        lastname1 = request.form.get('lastname1')
        lastname2 = request.form.get('lastname2')
        email = request.form.get('email')
        street = request.form.get('street')
        number = request.form.get('number')
        colony = request.form.get('colony')
        city = request.form.get('city')
        codigoPostal = request.form.get('codigoPostal')
        telephone = request.form.get('telephone')
        curp = request.form.get('curp')
        rfc = request.form.get('rfc')
        type = request.form.get('type')
        password = request.form.get('password')
        try:
            user = User(email=email, name=name, password=password, street=street, number=number, colony =colony, city=city, telephone=telephone, type=type, lastname1=lastname1, lastname2=lastname2, codigoPostal=codigoPostal, curp=curp, rfc=rfc)
            user0 = User.query.filter_by(email=email).first()
            user1 = User.query.filter_by(curp=curp).first()
            user2 = User.query.filter_by(rfc=rfc).first()
            if user0.id != id or user1.id != id or user2.id != id:
                flash('EL usuario ya existe')
            else:
                updateUser.name = name
                updateUser.lastname1 = lastname1
                updateUser.lastname2 = lastname2
                updateUser.email = email
                updateUser.street = street
                updateUser.number = number
                updateUser.colony = colony
                updateUser.city = city
                updateUser.codigoPostal = codigoPostal
                updateUser.telephone = telephone
                updateUser.type = type
                updateUser.curp = curp
                updateUser.rfc = rfc
                updateUser.password = password
                db.session.commit()
                flash('Usuario actualizado correctamente')
                return redirect(url_for('admin.dashboard'))
        except:
            flash('Error: ya existe un usuario con alguno de esos datos')
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
        lastname1 = request.form.get('lastname1')
        lastname2 = request.form.get('lastname2')
        curp = request.form.get('curp')
        nss = request.form.get('nss')
        street = request.form.get('street')
        number = request.form.get('number')
        colony = request.form.get('colony')
        city = request.form.get('city')
        codigoPostal = request.form.get('codigoPostal')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        salary = request.form.get('salary')
        date = request.form.get('date')
        try:
            employee = Employee(name=name, email=email, lastname1=lastname1, lastname2=lastname2, curp=curp, nss=nss, street=street, number=number, colony=colony, city=city, codigoPostal=codigoPostal, telephone=telephone, salary=salary, date=date)
            employee1 = Employee.query.filter_by(email=email).first()
            employee2 = Employee.query.filter_by(curp=curp).first()
            employee3 = Employee.query.filter_by(nss=nss).first()

            if employee1.id != id or employee2.id != id or employee3.id != id:
                flash('Error: algunos de los datos pertenecen a otro empleado')
            else:
                updateEmployee.name = name
                updateEmployee.email = email
                updateEmployee.lastname1 = lastname1
                updateEmployee.lastname2 = lastname2
                updateEmployee.curp = curp
                updateEmployee.nss = nss
                updateEmployee.street = street
                updateEmployee.number = number
                updateEmployee.colony = colony
                updateEmployee.city = city
                updateEmployee.codigoPostal = codigoPostal
                updateEmployee.telephone = telephone
                updateEmployee.date = date
                updateEmployee.salary = salary
                db.session.commit()
                flash('Empleado actualizado correctamente')
                return redirect(url_for('admin.dashboard'))
        except:
            flash('Error: ya existe un empleado con alguno de esos datos')
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
        flash('Pedido actualizado correctamente')
        return redirect(url_for('admin.dashboard'))
    
    updateOrder = Order.query.filter_by(id=id).first()
    users = User.query.all()
    products = Product.query.all()
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

