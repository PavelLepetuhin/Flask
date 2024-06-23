import requests

# response = requests.post('http://127.0.0.1:5000/ads/', json={
#     "title": "Title1",
#     "description": "Description1",
#     "owner": "Owner1"
# })
#
# print(response.status_code)
# print(response.text)


response = requests.get('http://127.0.0.1:5000/ads/1/')

print(response.status_code)
print(response.json())


response = requests.delete('http://127.0.0.1:5000/ads/1/')

print(response.status_code)
print(response.json())

response = requests.get('http://127.0.0.1:5000/ads/1/')

print(response.status_code)
print(response.json())