import configparser
import googlemaps


config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['googlemaps']['api_key']
gmaps = googlemaps.Client(key=api_key)

def get_coordinates_google(address):

    # Geocode the address
    result = gmaps.geocode(address)

    if result:
        location = result[0]['geometry']['location']
        return (location['lat'], location['lng'])
    return None


