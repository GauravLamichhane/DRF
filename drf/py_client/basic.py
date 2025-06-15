import requests # type: ignore


endpoint = "http://localhost:8000/api/"

get_response = requests.get(endpoint,json={"query":"hello world"})
# print(get_response.text)
# print(get_response.json())
# print(get_response.headers)
print(get_response.text)