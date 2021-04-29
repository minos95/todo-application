from todo import db,bcrypt,login_manager
from flask_login import UserMixin
import datetime
#ce fiechier contient tous les models de la base de donnee

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):  #cree une table User avec different attribue ci-dessus
    id= db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,)
    email=db.Column(db.String(length=30),nullable=False,unique=True)
    password=db.Column(db.String(length=100),nullable=False)
    todos=db.relationship('Todo',backref='owned_user',lazy=True)
    @property
    def pwd(self):
        return self.pwd
    @pwd.setter
    def pwd(self, plain_text_password):
        self.password=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password,attempted_password)
class Todo(db.Model):   # cree une table Todo avec different attribue ci-dessus
    id= db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False)
    category=db.Column(db.String(length=30),nullable=False,)
    share=db.Column(db.Boolean(),nullable=False,default=False)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))
    date_added=db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Space(db.Model):   # cree une table Todo avec different attribue ci-dessus
    id= db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False)