__author__ = 'Nick'
from flask import Flask, request, session, redirect, flash, render_template, g, url_for
from flask_admin import Admin
from model import *
import requests

app = Flask(__name__)
app.secret_key = 'asdI@YjUa+563ioP!98(/aAraA12NosMl;'

"""
HOME PAGE
"""
@app.route('/')
def index():
   return render_template('index.html')

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
    print(thehobby.name)
    if thehobby:
        return render_template('hobby.html',hobby=thehobby)
    return redirect(url_for('browse'))

"""
REGISTER USER
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      use = User.create(username=request.form['username'],
                        firstname=request.form['firstname'],
                        lastname=request.form['lastname'],
                        password=request.form['password'],
                        email=request.form['email'])
      return redirect(url_for('index'))
   return render_template('register.html')

"""
LOGIN
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      use = User.select().where(request.form['username'] == User.username,
                                request.form['password'] == User.password).get()

      if use:
         print("user exists")
         session['username'] = use.username
         session['userid'] = use.id
         flash("You have successfully logged in!")
         return redirect(url_for('index'))
      else:
         print("no user")
   return render_template('login.html')

"""
LOGOUT
"""
@app.route('/logout')
def logout():
   session.pop("username", None)
   session.pop("user", None)
   flash("You are now logged out.")
   return redirect(url_for("index"))

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
