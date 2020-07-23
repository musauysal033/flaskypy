from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from wtform_fields import *
from models import *

#confirm app
app= Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://wackgzxnaxzann:ab7da9f7238d09c196ae6db9c3ce87a15f228d85accbfc453d2790b818d0c9c4@ec2-52-31-233-101.eu-west-1.compute.amazonaws.com:5432/de5tc62jsm4k4m'
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    # update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # hash password
        hashed_password = pbkdf2_sha256.hash(password)


        # add user to db
        user =User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("index.html",form=reg_form)

@app.route("/login", methods=['GET','POST'])
def login():

    login_form = LoginForm()

    #Allow login  if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

        return "Not logged in with :("

    return render_template("login.html",form =login_form)

@app.route("/chat",methods=['GET','POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please login before accessing "

    return "chat with me"


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return "logged out using flask-login!"
if __name__ == "__main__":
    app.run(debug=True)
