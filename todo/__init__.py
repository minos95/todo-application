from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt         #bibliotheque pour crypte
from flask_login import LoginManager    #bibliotheque pour l'authentification 

    

app= Flask(__name__)

#configuration de la base de donne
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY']='370fea70834bba1468d28654'
db=SQLAlchemy(app)
#bcrypt pour crypter les mot de passes
bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
from todo import routes