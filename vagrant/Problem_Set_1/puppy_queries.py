from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# QUERY 1: Query all of the puppies and return the results in ascending alphabetical order
query_1 = session.query(Puppy.name).order_by(Puppy.name.asc())

print "QUERY 1"
for q in query_1.all():
	print q[0]

# QUERY 2: Query all of the puppies that are less than 6 months old organized by the youngest first
today = datetime.date.today()
sixMonthsAgo = today - datetime.timedelta(days = 182)

query_2 = session.query(Puppy.name, Puppy.dateOfBirth)\
	.filter(Puppy.dateOfBirth >= sixMonthsAgo)\
	.order_by(Puppy.dateOfBirth.desc())

print "QUERY 2"
for q in query_2.all():
	print q[0], q[1]

# QUERY 3: Query all puppies by ascending weight
query_3 = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc())

print "QUERY 3"
for q in query_3.all():
	print q[0], q[1]

# QUERY 4: Query all puppies grouped by the shelter in which they are staying
query_4 = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id)

print "QUERY 4"
for q in query_4.all():
	print q[0].name, q[1]