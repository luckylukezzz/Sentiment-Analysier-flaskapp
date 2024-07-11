import requests
r = requests.get('http://httpbin.org/headers')
print(r.json())