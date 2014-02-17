__author__ = 'Nick'
from peewee import *
import datetime
import json

db = PostgresqlDatabase('hobbydb', user='hobbyuser', password='hobbypassword', host='localhost')

class PostgresqlModel(Model):
   """A base model that will use our Postgresql database"""
   class Meta:
      database = db

#user information for now
class User(PostgresqlModel):
   id = PrimaryKeyField()
   firstname = CharField(default="")
   lastname = CharField(default="")
   username = CharField(default="")
   password = CharField(default="")
   email = CharField(default="")
   datecreated = DateTimeField(default=datetime.datetime.now())
   admin = BooleanField(default=False)

#hobby that exists
class Hobby(PostgresqlModel):
   id = PrimaryKeyField()
   name = CharField(default="")
   description = CharField(default="")
   imageurl = CharField(default="")
   links = CharField(default="")

class Rating(PostgresqlModel):
   id = PrimaryKeyField()
   rating = IntegerField(default=1)
   hobbyid = ForeignKeyField(Hobby)
   userid = ForeignKeyField(User)

class Review(PostgresqlModel):
   id = PrimaryKeyField()
   text = CharField(default="")
   postdate = DateTimeField(default=datetime.datetime.now())
   userid = ForeignKeyField(User)
   hobbyid = ForeignKeyField(Hobby)

class MyHobbies(PostgresqlModel):
   id = PrimaryKeyField()
   userid = ForeignKeyField(User)   #keep list of users hobbies(following?)
   hobbyid = ForeignKeyField(Hobby)  #hobby foreign key

class MyHobbyUpdates(PostgresqlModel):
   id = PrimaryKeyField()
   updatefrom = ForeignKeyField(User)   #update from user
   myhobbyid = ForeignKeyField(MyHobbies)    #myhobby foreign key
   title = CharField(default="")    #title of update
   link = CharField(default="")     #optional link
   text = CharField(default="")     #optional text
   updatedate = DateTimeField(default=datetime.datetime.now())
   publish = BooleanField(default=False) #publish to the hobby wall