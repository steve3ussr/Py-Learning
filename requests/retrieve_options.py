import requests



url = 'https://www.google.com'
s = requests.session()
resp = s.options(url)

print(resp)
