__author__ = 'Nick'
from flask import Flask, request, session, redirect, flash, render_template, g, url_for
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
from flask_admin import Admin
from passlib.hash import sha256_crypt
from model import *
import requests
import os

app = Flask(__name__)
app.secret_key = 'asdI@YjUa+563ioP!98(/aAraA12NosMl;'

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

"""
HOME PAGE
"""
@app.route('/')
def index():
   if current_user.is_authenticated():
      return render_template('index.html')
   else:
      return redirect(url_for("login"))
"""
ADD HOBBY
"""
@app.route('/addhobby', methods=['GET', 'POST'])
def addhobby():
   if request.method == 'POST':
      hob = Hobby.create(name=request.form['name'],
                         description=request.form['desc'],
                         imageurl=request.form['url'])
      return redirect(url_for('browse'))
   return render_template('addhobby.html')

"""
BROWSE HOBBIES
"""
@app.route('/browse')
def browse():
    hlist = Hobby.select()
    return render_template('browse.html', hobbyList=hlist)

"""
HOBBY DETAIL
"""
@app.route('/hobby/<hid>')
def hobby(hid):
    if not hid:
        return redirect(url_for('browse'))
    thehobby = Hobby.select().where(hid == Hobby.id).get()
    if thehobby:
        return render_template('hobby.html',hobby=thehobby)
    return redirect(url_for('browse'))

"""
FOLLOW HOBBY
"""
@app.route('/followhobby/<hid>')
def followhobby(hid):
   hobb = MyHobbies.create(userid=current_user.id,
                           hobbyid=hid)
   return redirect(url_for('user', userid=current_user.id))


"""
REGISTER USER
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      pass_hash = sha256_crypt.encrypt(request.form['password'])
      use = User.create(username=request.form['username'],
                        firstname=request.form['firstname'],
                        lastname=request.form['lastname'],
                        password=pass_hash,
                        email=request.form['email'])
      return redirect(url_for('index'))
   return render_template('register.html')

"""
LOGIN
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      use = User.select().where(request.form['username'] == User.username).get()

      if use:
         login_test = sha256_crypt.verify(request.form['password'], use.password)
         if login_test:
            print("user exists")
            login_user(use, True)
            flash("You have successfully logged in!")
            return redirect(url_for('index'))
         else:
            flash("Invalid username / password combination.", 'danger')
      else:
         flash("Invalid username / password combination.", 'danger')
   return render_template('login.html')

"""
LOGOUT
"""
@app.route('/logout')
def logout():
   logout_user()
   flash("You are now logged out.")
   return redirect(url_for("index"))

"""
USER DETAIL
"""
@app.route('/user/<userid>')
def user(userid):
   use = User.select().where(userid == User.id).get()
   hbs = Hobby.select().join(MyHobbies).where((userid == MyHobbies.userid) & (Hobby.id == MyHobbies.hobbyid))
   return render_template("user.html", user=use, hobs=hbs)

"""
LIST USERS
"""
@app.route('/users')
def users():
   userList = User.select()
   return render_template('userlist.html', users=userList)

#DATABASE
#open/close db before/after connection
@app.before_request
def before_request():
   g.db = db
   g.db.connect()

@app.after_request
def after_request(response):
   g.db.close()
   return response

#START
if __name__ == '__main__':
   app.run(debug=True, host="127.0.0.1")
