from flask import Blueprint 
from .controller import login_controller

login_bp= Blueprint('login', __name__, url_prefix='/api/auth')
@login_bp.post('/login')
def login():
    return login_controller()# controller retorna lo que el service haga 

# @login_bp.post('/register')
# def register():
#     return register_controller()# controller retorna lo que el service haga 
