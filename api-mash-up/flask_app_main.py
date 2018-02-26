# flask_app_main_py
# the main flask application to help testing the rest of the apis

from findARestaurant import findARestaurant
from restaurant_db_setup import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# setup flask and the database
app = Flask(__name__)
engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# ROUTES
app.route('/restaurants', method=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        # We want to return all restaurants
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[i.serialize for i in restaurants])

    elif request.method == 'POST':
        


# Application Start Point
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
