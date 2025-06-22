import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data = {
  "title":"This field is the title after update update",
  "price":129.99
}

get_response = requests.put(endpoint,json = data)

print(get_response.json())