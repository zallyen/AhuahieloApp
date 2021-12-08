from functools import wraps
from flask import url_for, request, redirect, session
from flask_login import login_required, current_user
from .models import *

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(session.get('email'))
            if session.get('email')==None:
                return redirect(url_for('auth.login'))

            user = current_user
            print(user)
            if not is_admin(user):
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def is_admin(user):
        return user.type == 'Administrador'


                 

    
    