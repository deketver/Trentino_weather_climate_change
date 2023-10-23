import os


AMBEE_API_KEY = os.environ.get('AMBEE_API_KEY')

print(AMBEE_API_KEY)
AMBEE_API_KEY = ''

import http.client

conn = http.client.HTTPSConnection("api.ambeedata.com")

headers = {
    'x-api-key': AMBEE_API_KEY,
    'Content-type': "application/json"
    }

conn.request("GET", "/history/by-lat-lng?lat=46.0714197&lng=11.1264842&from=2015-07-13%2012%3A16%3A44&to=2020-07-14%2012%3A16%3A44", headers=headers)

res = conn.getresponse()
print(res.status)
data = res.read()
print(data.decode("utf-8"))