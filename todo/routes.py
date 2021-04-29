# ce fichier contient toute les routes  (Backend)


from todo import app,db
from flask import render_template,request,redirect,url_for,flash
from todo.forms import RegisterForm,TodoForm,SignInFrom,SpaceForm
from todo.models import Todo,User,Space
from flask_login import login_user,logout_user,login_required,current_user
from sqlalchemy import or_,desc 
@app.route('/',methods=['GET','POST']) #cree une route qui accepte les methode get et post
@app.route('/index',methods=['GET','POST'])# la route / et /index c'est la meme route
def index_page():
    form=SignInFrom() #SignInForm se trouve dans fichier forms 
    if form.validate_on_submit(): #si toute les input du formulaire sont valider et submit
        attempted_user=User.query.filter_by(name=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('vous ete enregistrer avec succes !!',category="success")
            return redirect (url_for('dashboard_page'))
        else:
            flash("Nom d'utilisateur ou mot de passe ne sont pas correct",category='danger')
    return render_template('index.html',nonavbar="",form=form) #fonction pour afficher les template html avec les paramter
    #non navbar pour que le navbar ne s'affiche pas et form pour le formalaire


@app.route('/signIn',methods=['GET','POST'])
def signIn_page():
    form=RegisterForm()
    if form.validate_on_submit():
        print('form executed')
        
        user_to_create=User(name=form.username.data,
                            email=form.email.data,
                            pwd=form.password1.data,
       
                                 )
        db.session.add(user_to_create)
        db.session.commit()
        print('db executed')
        return redirect(url_for('index_page'))
    if form.errors!={}:
        for err_msg in form.errors.values():
                print(err_msg)
                flash(" erreur: {}".format(err_msg),category='danger')
    return render_template('signIn.html',nonavbar="",form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard_page():
    id=current_user.id
    todos=Todo.query.order_by(desc(Todo.id)).filter_by(owner=id).all()
    if request.args.get("action")=="delete":
        id_todo=request.args.get("todo")
        todo=Todo.query.filter_by(id=id_todo).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('dashboard_page'))

    if request.args.get("action")=="share":
        id_todo=request.args.get("todo")
        todo=Todo.query.filter_by(id=id_todo).first()
        todo.share=True
        db.session.commit()
    return render_template('dashboard.html',todos=todos)

@app.route('/addTodo',methods=['GET','POST'])
@login_required
def addTodo_page():
    form=TodoForm()
    id=current_user.id
    #request.args.get("user")
    if request.args.get("action")=='add':
        if form.validate_on_submit():
            print('form executed')
            
            todo_to_create=Todo(name=form.name.data,
                                category=form.category.data,
                                owner=id
                                    
                                    )
            db.session.add(todo_to_create)
            db.session.commit()
            print('db executed')
            return redirect(url_for('dashboard_page',page_num=1))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(err_msg)
    if request.args.get("action")=="edit":
        idTodo=request.args.get("todo")
        todo=Todo.query.filter_by(id=idTodo).first()
        if form.validate_on_submit():
            todo.name=form.name.data
            todo.category=form.category.data
            db.session.commit()
            return redirect(url_for('dashboard_page'))
        return render_template('addTodo.html',form=form,todo=todo,action='edit')

    return render_template('addTodo.html',form=form)

@app.route('/addSpace',methods=['GET','POST'])
@login_required
def addSpace_page():
    form=SpaceForm()
    if form.validate_on_submit():
        
        space_to_create=Space(name=form.name.data  )
        db.session.add(space_to_create)
        db.session.commit()
        print('db executed')
        return redirect(url_for('dashboard_page'))
            
    return render_template('addSpace.html',form=form)

@app.route('/world',methods=['GET','POST'])
@login_required
def world_page():
    
    todos=Todo.query.order_by(desc(Todo.id)).join(User,Todo.owner==User.id).filter(Todo.share==True).all() # requete pour recupere les todo partager
    
    return render_template('world.html',todos=todos)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('index_page'))
