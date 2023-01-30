from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('log_in.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_regist(request.form):
        # we redirect to the template with the form.
        return redirect('/')  
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(user_data)
    print(user_id)
    session['user_id'] = user_id # this equals the id
    
    return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid Email/Password!","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password!", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')


@app.route('/success')
def logged_in():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('profile.html', user = User.get_one(data), all_the_posts = Post.get_all_posts_with_creator())

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')

# @app.route('/create_post', methods = ['POST'])
# def save():
#     data = {
#         "user_id": request.form['user_id'],
#         "content": request.form['content']
#     }
#     Post.save(data)
#     return redirect('/success')