# flask_app_main_py
# the main flask application to help testing the rest of the apis

from findARestaurant import findARestaurant
from restaurant_db_setup import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import codecs

# setup flask and the database
app = Flask(__name__)
engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# ROUTES
# we want to be able to get all restaurants from the database
# AND we want to be able to provide arguments in the url to add items to the data base
@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        # We want to return all restaurants
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[i.serialize for i in restaurants])

    elif request.method == 'POST':
        # make a new restaurant and put it in the data base
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        restaurant_info = findARestaurant(mealType, location)
        if restaurant_info != "No Restaurants Found": # we found a restaurnt based on the arguments
            restaurant = Restaurant(restaurant_name=(restaurant_info['name']).encode(),
                                    restaurant_address=(restaurant_info['address']).encode())
            # for the above function we need to cover the case where we get non standard characters .encode() force
            # converts what ever is in the JSON object into unicode as the .encode() default is UTF-8
            session.add(restaurant)
            session.commit()
            return jsonify(restaurant=restaurant.serialize)
        else:
            return jsonify({"Error": "No Restaurants found for " + mealType + "in " + location})


# Here we want to make sure we can GET, UPDATE or DELETE a specific restaurant
@app.route('/restaurants/<int:id>', methods=['GET', 'POST', 'DELETE'])
def restaurant_handler(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'GET':
        # return the specific restaurant we just queried for
        return jsonify(restaurant=restaurant.serialize)
    elif request.method == 'POST':
        # here we will update a specific restaurant entry
        address = request.args.get('address')
        name = request.args.get('name')
        image = request.args.get('image')
        # check and re-assign values with new values
        if address:
            restaurant.restaurant_address = address
        if name:
            restaurant.restaurant_name = name
        if image:
            restaurant.restaurant_image = image
        session.commit()
        # now that we have everything adjusted and committed return the json object
        return jsonify(restaurant=restaurant.serialize)
    elif request.method == 'DELETE':
        # obviously here we need to delete the specified restaurant
        session.delete(restaurant)
        session.commit()
        return "Restaurant Deleted"


# Application Start Point
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
