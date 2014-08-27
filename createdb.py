__author__ = 'Nick Sjostrom'
from model import *

tables = [User, Hobby, Rating, MyHobbies, HobbyImages, HobbyLinks, HobbyComment]

for table in tables:
   if table.table_exists():
      pass#table.drop_table()
   else:
      table.create_table()