import requests


url = 'https://httpbin.org/cookies/set'
req = requests.Request(method="GET", url=url, params={'username': 'steve', 'password': 'qwerty'}).prepare()
print(req.url)
session = requests.Session()
resp1 = session.send(req)
print(resp1.cookies)

url = 'https://httpbin.org/cookies'
resp2 = requests.get(url=url)
print(resp2.cookies)
