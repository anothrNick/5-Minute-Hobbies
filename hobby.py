__author__ = 'Nick'
from flask import Flask, request, session, redirect, flash, render_template, g, url_for
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
from flask_admin import Admin
from passlib.hash import sha256_crypt
from model import *
from forms import *
from flaskext.markdown import Markdown
import requests
import os

app = Flask(__name__)
app.secret_key = 'asdI@YjUa+563ioP!98(/aAraA12NosMl;'

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

Markdown(app)
"""
HOME PAGE
"""
@app.route('/')
def index():
   if current_user.is_authenticated():
      return redirect(url_for("browse"))
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
   cnt = MyHobbies.select().where(MyHobbies.userid==current_user.id, MyHobbies.hobbyid==hid).count()

   if not cnt:
      hobb = MyHobbies.create(userid=current_user.id,
                              hobbyid=hid)
   return redirect(url_for('user', userid=current_user.id))

@app.route('/hobby/pic/<hid>', methods=['GET', 'POST'])
def hobby_pic(hid):
   if request.method == 'POST':
      if request.form['image'] != "":
         hob = HobbyImages.create(imageurl=request.form['image'],
                                  desc=request.form['desc'],
                                  hobbyid=hid)
   return redirect(url_for("hobby", hid=hid))

@app.route('/hobby/desc/<hid>', methods=['GET', 'POST'])
def hobby_desc(hid):
   if request.method == 'POST':
      if request.form['desc-edit'] != "":
         hob = Hobby.select().where(Hobby.id==hid).get()
         if hob:
             hob.description = request.form['desc-edit']
             hob.save()
   return redirect(url_for("hobby", hid=hid))


"""
REGISTER USER
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
   form = RegisterForm()

   if form.validate_on_submit():
      pass_hash = sha256_crypt.encrypt(form.password.data)
      use = User.create(username=form.username.data,
                        firstname=form.fname.data,
                        lastname=form.lname.data,
                        password=pass_hash,
                        email=form.email.data)
      return redirect(url_for('index'))
   return render_template('register.html', form=form)

"""
LOGIN
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm()

   print(form.username.data)
   print(form.password.data)
   if form.validate_on_submit():
      try:
         use = User.select().where(form.username.data == User.username).get()
         print(form.password.data)
         if use:
            login_test = sha256_crypt.verify(form.password.data, use.password)
            if login_test:
               login_user(use, True)
               flash("You have successfully logged in!")
               return redirect(url_for('index'))
            else:
               raise Exception()
         else:
            raise Exception()
      except:
         flash("Invalid username / password combination.", 'danger')

   return render_template('login.html', form=form)

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

@lm.user_loader
def load_user(id):
   try:
      return User.get(User.id == id)
   except:
      return None


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
