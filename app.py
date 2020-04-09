import requests,json

url="https://covid19-kerala-api.herokuapp.com/api/location?date=latest"
data=requests.get(url)
data=data.json()
json_string = json.dumps(data)
y=json.loads(json_string)
print()
