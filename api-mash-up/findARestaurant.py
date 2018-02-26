from geocode import get_Geocode_Location
import json
import httplib2
import api_keys

# NOTE ON IMPORTS
# Importing sys and codecs causes a system level error to get thrown in codecs.py in the write function
# not really sure what is causing the issue.
# import sys
# import codecs

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = api_keys.foursquare_api_key['client_id']
foursquare_client_secret = api_keys.foursquare_api_key['client_secret']
foursquare_version = api_keys.foursquare_api_key['version']


def findARestaurant(mealType, location):

    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    lat, long = get_Geocode_Location(location)
    # print(lat, long)
    # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    url = "https://api.foursquare.com/v2/venues/search?client_id=" + foursquare_client_id + "&client_" \
        "secret=" + foursquare_client_secret + "&v=" + foursquare_version + "&ll=" + str(lat) + "," + str(long) + "&query=" + mealType
    # create HTTP handler and load response in json
    # print(url)
    http_handler = httplib2.Http()
    result = json.loads(http_handler.request(url, 'GET')[1])

    # 3. Grab the first restaurant
    if result['response']['venues']:
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        # since 'formattedAddress' is another dictionary we need to parse over it and put it one string
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address
        # 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300
        # value in the URL or replacing it with 'original' to get the original picture
        url = "https://api.foursquare.com/v2/venues/" + venue_id + "/photos?&client_id=" + foursquare_client_id + "&client_" \
        "secret=" + foursquare_client_secret + "&v=" + foursquare_version
        # print(url)
        result = json.loads(http_handler.request(url, 'GET')[1])
        # 5. Grab the first image
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
            # 6. If no image is available, insert default a image url
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
        # 7. Return a dictionary containing the restaurant name, address, and image url
        restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': imageURL}
        print("Restaurant Name: ", restaurant_info['name'])
        print("Restaurant Address: ", restaurant_info['address'])
        print("Restaurant Picture: ", restaurant_info['image'])
        return
    else:
        print("No Restaurant Found for: ", location)
        return "No Restaurants Found"


if __name__ == '__main__':
    print("start")
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
    print("Finish")
