__author__ = 'Nick'
from peewee import *
import peewee
import datetime
import json

#sqlite
db = peewee.SqliteDatabase('data.db', threadlocals=True)

class dbModel(Model):
   """A base model that will use our sqlite database"""
   class Meta:
      database = db

#user information for now
class User(Model):
   id = PrimaryKeyField()
   firstname = CharField(default="")
   lastname = CharField(default="")
   username = CharField(default="")
   password = CharField(default="")
   email = CharField(default="")
   avatar = CharField(default="")
   datecreated = DateTimeField(default=datetime.datetime.now())
   admin = BooleanField(default=False)
   active = BooleanField(default=True)

   def is_authenticated(self):
      return True

   def is_active(self):
      return self.active

   def is_anonymous(self):
      return False

   def get_id(self):
      return str(self.id)

   def __str__(self):
      return self.lastname

#hobby that exists
class Hobby(Model):
   id = PrimaryKeyField()
   name = CharField(default="")
   description = TextField(default="")
   imageurl = CharField(default="")
   creator = ForeignKeyField(User, related_name="user")

class HobbyImages(Model):
   id = PrimaryKeyField()
   desc = CharField(default="")
   imageurl = CharField(default="")
   hobbyid = ForeignKeyField(Hobby, related_name="images")

class HobbyLinks(Model):
   id = PrimaryKeyField()
   link = TextField(default="")
   title = CharField(default="")
   hobbyid = ForeignKeyField(Hobby, related_name="links")

class Rating(Model):
   id = PrimaryKeyField()
   rating = IntegerField(default=1)
   hobbyid = ForeignKeyField(Hobby)
   userid = ForeignKeyField(User)

class MyHobbies(Model):
   id = PrimaryKeyField()
   userid = ForeignKeyField(User)   #keep list of users hobbies(following?)
   hobbyid = ForeignKeyField(Hobby)  #hobby foreign key

class HobbyComment(Model):
   id = PrimaryKeyField()
   userid = ForeignKeyField(User, related_name="usercomments")
   hobbyid = ForeignKeyField(Hobby, related_name="hobbycomments")
   date = DateTimeField(null=True)
   comment = TextField(default="")
