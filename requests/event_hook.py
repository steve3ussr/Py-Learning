import requests


def h(resp: requests.Response, *args, **kwargs):
    print(f"{resp}, {resp.status_code}")
    print(args)
    print(kwargs)
    return resp

url = 'https://www.google.com'
s = requests.session()
s.hooks['response'].append(h)
s.get(url)
