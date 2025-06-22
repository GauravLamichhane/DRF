import requests
from getpass import getpass
auth_endpoint = "http://localhost:8000/api/auth/"
username = input("Enter the username:")
# password = input("Enter the password:")
password = getpass()
auth_response = requests.post(auth_endpoint,json={'username':username,'password':password})
print(auth_response.json())

if auth_response.status_code == 200:
  token = auth_response.json()['token']#acessing the token key in the dictionary
  headers = {
    "Authorization": f"Bearer {token}"#standard, required by drf authorizaion nai use garnw parxa
  }
  endpoint ="http://localhost:8000/api/products/"
  get_response = requests.get(endpoint, headers= headers)
  print(get_response.json())