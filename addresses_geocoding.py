# Found that my teachersapp/resources/dummy-users.txt file has
# somewhat ureliable coordinates, so I will use this script to 
# get new latitude/longitude coordinates for each user address
# by querying Google's Geocoding API (https://developers.google.com/maps/documentation/geocoding/start) 
# (make sure you enable this API for your project)

from urllib import parse
import requests
from teachersapp import create_app, db

app = create_app()
app.app_context().push()

# I will collect the updated users in an array, so I can store that in a new file at the end
updated_users = []

with open("teachersapp/resources/dummy-users.txt", "r") as a_file:
  for line in a_file:
    givenName,streetAddress,city,email,username,latitude,longitude = line.strip().split(",")

    # The streetAddress and city in the file might be surrounded by double quotes,
    # so I want to strip those out before sending to Google. 
    full_address = streetAddress.replace('"', '')+", "+city.replace('"', '')
    params = {'address': full_address, 'key': app.config['GOOGLE_MAPS_API_KEY']}
    query_url = "https://maps.googleapis.com/maps/api/geocode/json?" + parse.urlencode(params)

    #print('Requesting coordinates for', full_address)

    try:
        response = requests.get(query_url, timeout=15)
    except:
        print('Exception calling api for', full_address)   
        response = None 

    if response != None and response.ok:
        response_json = response.json()
        #print(response_json)

        # The API can return multiple results per query.
        # I will take the first always but in reality
        # if these were true addresses I should come up with 
        # a better logic to only pick the right result, log it, 
        # or ignore it if I cannot determine if it is correct
        if len(response_json['results']) > 0:
            result = response_json['results'][0]
            new_address = result['formatted_address'].replace(',', ';') # dont want to break csv format
            new_latitude = result['geometry']['location']['lat']
            new_longitude = result['geometry']['location']['lng']
            location_type = result['geometry']['location_type']

            # location_type = APPROXIMATE is just the center of a city / town
            # I do not want multiple users piling up in same approximate points so
            # these will be ignored.
            if (location_type == 'APPROXIMATE'):
                print('IGNORING', 'Old address', full_address, 'New address', location_type, new_address)
                continue

            print('Old address', full_address, latitude, longitude, 'New address', new_address, new_latitude, new_longitude)
            updated_users.append(line.rstrip() + ',' + new_address + ',' + str(new_latitude) + ',' + str(new_longitude))
        else:
            print('NOT FOUND', full_address)

    else:
        print("ERROR getting coordinates for address", full_address)   


# Write results to a new file
with open("teachersapp/resources/dummy-users-v2.txt", "w") as txt_file:
    for user_line in updated_users:
        txt_file.write(user_line + "\n") 