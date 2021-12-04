from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, make_response, session
from flask_login import login_required, current_user
from .models import *
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    products = Product.query.all()
    orders = Order.query.filter_by(customerId=current_user.id)
    return render_template('home.html', products=products, orders=orders, user=current_user)

@views.route('/product/<id>', methods=['GET', 'POST'])
@login_required
def product(id):
    item = Product.query.filter_by(id=id).first()
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        address = request.form.get('address')
        order = Order(customerId=current_user.id, productId=id, quantity=quantity, date=date.today(), total=item.price*int(quantity), address=address)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('product.html', product=item)

def producd(id):
    return Product.query.filter_by(id=id).first()

@views.route('/order/<id>', methods=['GET', 'POST'])
@login_required
def order(id):
    order = Order.query.filter_by(id=id).first()
    return render_template('order.html', order=order, get_product = producd)

@views.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))