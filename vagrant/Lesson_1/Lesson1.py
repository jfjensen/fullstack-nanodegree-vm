import sqlalchemy
import database_setup

engine = sqlalchemy.create_engine('sqlite:///restaurantmenu.db')
database_setup.Base.metadata.bind = engine
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()

for e in session.query(database_setup.Restaurant).all():
	e.name

items = session.query(database_setup.MenuItem).all()
	for item in items:
	    print item.name

for item in items:
    print item.name, item.course

veggieBurgers = session.query(database_setup.MenuItem).filter_by(name='Veggie Burger')
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print "\n"

UrbanVeggieBurger = session.query(database_setup.MenuItem).filter_by(id=8).one()
print UrbanVeggieBurger.price

UrbanVeggieBurger = session.query(database_setup.MenuItem).filter_by(id=9).one()
print UrbanVeggieBurger.price                                               $5.99
print UrbanVeggieBurger.name

UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

veggieBurgers = session.query(database_setup.MenuItem).filter_by(name='Veggie Burger')
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print "\n"

for veggieBurger in veggieBurgers:
	if veggieBurger.price != '$2.99':
		veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()

veggieBurgers = session.query(database_setup.MenuItem).filter_by(name='Veggie Burger')
for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print "\n"     


spinach = session.query(database_setup.MenuItem).filter_by(name='Spinach Ice Cream').one()
print spinach.restaurant.name

session.delete(spinach)
session.commit()
spinach = session.query(database_setup.MenuItem).filter_by(name='Spinach Ice Cream').one()
