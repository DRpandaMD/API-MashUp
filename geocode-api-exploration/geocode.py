# geocode api app

import api_keys
import httplib2
import json

def get_Geocode_Location(inputString):
    key = api_keys.google_api_key['client_id']
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=' + locationString +
           '&key=' + key)
    #print(url)
    http_handler = httplib2.Http()
    response, content = http_handler.request(url, 'GET')
    result = json.loads(content)
    lat = result['results'][0]['geometry']['location']['lat']
    long = result['results'][0]['geometry']['location']['lng']
    return lat, long
