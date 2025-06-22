import requests


headers = {'Authorization':'Bearer ab2a485aa1a19eccfdf47b31434fbb5b7c5bd53c'}

endpoint = "http://localhost:8000/api/products/"

data = {
  "title":"This field is done"
}

get_response = requests.post(endpoint,json = data, headers=headers)

print(get_response.json())