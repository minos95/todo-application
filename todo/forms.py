## dans ce dossier vous trouver toute les formulaire


from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import Length ,EqualTo,Email,DataRequired
from wtforms.fields.html5 import DateField
from todo.models import Space
print("+++++")
space=Space.query.all()
spaceChoices=[]
for elm in space:
    x=(elm.name,elm.name)
    spaceChoices.append(x)
    print(space)
    

class RegisterForm(FlaskForm):
    username=StringField(label="Nom D'utilisateur",validators=[Length(min=2,max=30),DataRequired()])
    email=StringField(label='Email Address',validators=[Email(),DataRequired()])
    password1=PasswordField(label='mot de passe',validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confimer votre mot de passe',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='submit')

class TodoForm(FlaskForm):
    def get_space(self):
        space1=Space.query.all()
        print('++++++++++++++++++++++')
        print(space1)
    name=StringField(label="Contenu Todo")
    category = SelectField(u'Espace', choices=spaceChoices)
    dt = DateField('DatePicker', format='%Y-%m-%d')
    submit=SubmitField(label='submit')

class SignInFrom(FlaskForm):
    username=StringField(label="Nom d'utilisateur")
    password=PasswordField(label='Mot de passe')
    submit=SubmitField(label='Enregistrer')

class SpaceForm(FlaskForm):
    name=StringField(label="ajouter un espace")
    submit=SubmitField(label='Enregistrer')