import sys
from pony.orm import *

from .settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

db = Database()

class Food(db.Entity):
    """ Food Class contains the data of openfoodfacts """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Set('Category')
    brands = Set('Brand')
    code = Required(str)
    nutriments = Required(Json)
    favor = Optional('Favor')

    def print_infos(self):
        print("Name : " + self.name)
        print("Description : " + self.code)
        print("Brands :")
        for brand in self.brands:
            print("\t- " + brand.name)

class Category(db.Entity):
    """ Category Class is connected to food by a many-to-many relation. """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)

class Brand(db.Entity):
    """ Brand Class is connected to food by a many-to-many relation. """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)

class Favor(db.Entity):
    """ Favor Class is connected to food by a one-to-one relation. """

    id = PrimaryKey(int, auto=True)
    food = Required(Food)

    def print_infos(self):
        print("Name : " + self.food.name)
        print("Description : " + self.food.code)
        print("Brands :")
        for brand in self.food.brands:
            print("\t- " + brand.name)

# Connect to database
db.bind(provider='mysql', host=MYSQL_HOST, user=MYSQL_USER,
    passwd=MYSQL_PASSWORD, db=MYSQL_DB)

# Generate database mapping and create tables if they doesn't exists
db.generate_mapping(create_tables=True)

# This lines delete and rebuild the tables if we fill the database
if(len(sys.argv) > 0):
    if('fill_database' in sys.argv):
        db.drop_all_tables(with_all_data=True)
        db.create_tables()
