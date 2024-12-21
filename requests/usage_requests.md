

# TODO

- [ ] test: convert method of post.data when formatting method not declared
- [ ] header overwrite instances
- [ ] Cert
- [ ] Auth
- [ ] session cookies policy: drop or merge?
- [ ] [Multipart-Encoded Files](https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)



# Quick Start

## make and send a request

> requests.[method]

- `get(url[, params])`
- `post(url[, data, json])`
- `put(url[, data])`
- `delete(url)`
- `head(url)`
- `options(url)`

## passing params & data

### get.params

- get.params receive dict of string pairs, `{'k1': 'v1', 'k2': 'v2'}`
- value can be a dict, `{'k', ['v1', v2']}` will make the URL be like: `url/index.html?k=v1&k=v2`

### post.json/data/file

> the `json` parameter is ignored if either `data` or `files` is passed

- `post.json` receive python dict object and auto convert it
- `post.data` can receive almost everything and auto convert it, unless explicitly declare the format in headers, like `application/text, application/json`
- `post.data` versus `post.json`: if use data, must use `data=json.dump(string)` and set headers as `application/json`; if use json, everything is so easy: no encode, no headers set

---

> It is strongly recommended that you open files in **binary mode**

file usages:

```python
files = {'file': open('report.xls')}

files = {'file': ('report.xls', 
                  open('report.xls'), 
                  'application/vnd.ms-excel', 
                  {'Expires': '0'}
                 )
        }
```



## other optional params

- `stream=True`
- `allow_redirects=False`
- `timeout=10`. **Nearly all production code should use this parameter in nearly all requests**



## Headers

Note that: 

- Custom headers are given **less precedence** than more specific sources of information
- Requests does not change its behavior at all based on which custom headers are specified. **The headers are simply passed on into the final request**.
- All header values must be a `string`, bytestring, or unicode. While permitted, it’s advised to avoid passing unicode header values.

Some instances:

- `Content-Length` will be overwritten if the content is determined
- etc. 







## get response

- `response.text`: auto decoded based on response headers
- `response.cotnent`: will show **binary response body**
- all compression contents are auto decoded (gzip, brotli, etc. )
- SPECIAL: response has a built-in json decoder, `response.json()`
- `response.raw`: get raw, compressed bytes
- `response.iter_content`: get raw, but un-compressed bytes -- which is recommended to **write them to a file-like object**
- 





# Request Object

- `req.url`
- two different ways to prepare:
  - `prepped=Request().prepare(), session.send(prepped)`, will not use any default params of sesion
  - `prepped=session.prepare_request()`

- edit `PreparedRequest`'s attrs, like headers or body
- 



# Response Object

## property

- `resp.text`
- `resp.encoding`: read/write an encoding method
- `resp.raw`
- `resp.headers`, *according to RFC 7230, header names are case-insenseitive*
- `resp.cookies`
- `resp.request`: yes, the `PreparedReqeust` is contains in a response object
- `resp.history`, a list of responses needed to complete the request

## method

`resp.raise_for_status()`: raise when resp is bad status like 4xx



# Session Object

Pros:

- persists params across requests
- use urllib3’s HTTP pool to mux connections, inc performances
- can be used as a ctx, which will make sure the session is closed

Default Params:

> Any dictionaries that you pass to a request method will be **merged** with the session-level values that are set. 
>
> The method-level parameters override session parameters.
>
> Note, however, that method-level parameters will *not* be persisted across requests, even if using a session, 
>
> Unless use the [Cookie utility functions](https://requests.readthedocs.io/en/latest/api/#api-cookies) to manipulate [`Session.cookies`](https://requests.readthedocs.io/en/latest/api/#requests.Session.cookies)

- `s.headers`: basic headers for all requests
- `s.cookies`: gen by requests







# Cookies

## Receive

Cookies in Requests stored in `RequestsCookieJar` object,  it works just like a python built-in dict.

note that `response.cookies` might be empty like:

```
response.cookies = <RequestsCookieJar[]>
```

**possible reason**: response is redirected, you can see `response.history` if there is a HTTP 302 response

**solution**: use session, cookies will be saved in session object; or track history





## Send

`requests.get(url, cookies=dict)`

# Errors and Exceptions

In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a [`ConnectionError`](https://requests.readthedocs.io/en/latest/api/#requests.ConnectionError) exception.

[`Response.raise_for_status()`](https://requests.readthedocs.io/en/latest/api/#requests.Response.raise_for_status) will raise an [`HTTPError`](https://requests.readthedocs.io/en/latest/api/#requests.HTTPError) if the HTTP request returned an unsuccessful status code.

If a request times out, a [`Timeout`](https://requests.readthedocs.io/en/latest/api/#requests.Timeout) exception is raised.

If a request exceeds the configured number of maximum redirections, a [`TooManyRedirects`](https://requests.readthedocs.io/en/latest/api/#requests.TooManyRedirects) exception is raised.

All exceptions that Requests explicitly raises inherit from [`requests.exceptions.RequestException`](https://requests.readthedocs.io/en/latest/api/#requests.RequestException).





# Stream, Keep-Alive and Chunk

## Body Content Workflow

by enabling `stream=True`, these will happen:

1. the header is downloaded immediately
2. the body will not be downloaded until access response.content



what you can achieve:

1. decide what to do according to headers
2. further control the workflow by using `resp.iter_lines/inter_content`, which return raw, un-compressed bytes



limits: if `stream=True`, the socket connection will not be closed unless:

1. call `resp.close`
2. consume all data
3. **better way**: use resp as a ctx

## History of Keep-Alive

> - https://en.wikipedia.org/wiki/Chunked_transfer_encoding
> - https://en.wikipedia.org/wiki/HTTP_persistent_connection

For HTTP/1.0, header `Connection: keep-alive` means the socket is kept open, which provides better performance; `Connection: close` means that it’s time to close, usually sent by client. 

For HTTP/1.1, connection is `keep-alive` by default; however, it may confuse client, make it hard to determine the start and the end of response (especially in streaming). 

Therefore another header is introduced: `Transfer-Encoding: chunked`. Response data is divided into non-overlapping chunks. The final chunk is zero-length, which end to transmission. 

When streaming (if chunked), `Content-Length` header is disabled, cause there is no need to know the length of response. 

## Send Chunked Request

**Easiest way**: make parameter data a generator. 



## Receive Chunked Response

call `resp.iter_content()` and return data chunk-by-chunk. Set `chunk_size=int` will limit max chunk size. 



# Event Hooks

Hook is essentially a callback function, can only be bound to response. A hook looks like: 

```python
def hook(resp, *args, **kw):
    print(resp)
    return resp

```

Note that: 

- If return None, then the hook will not modify response object; 
- If you want to change something, return the response
- args and kwargs must be set in arguments, because requests will pass timeout, proxy, stream etc. to the hook function. 

---

- How to define: `hooks_dict = {'response': [func1, func2]}`
- How to use 1: `requests.get(url, hooks=hooks_dict)`
- How to use 2: `session.hooks[response].append(func1)`



# Proxies

pass a dict object to `reqeusts.get` or `session`:

```python
proxies = {'http': 'http://10.10.1.10:3128',
           'https': 'http://10.10.1.10:1080', 
           'http': 'socks5:/'}

# 'http/https': 'scheme://user:pwd@host:port'
# socks5://user:pwd@172.0.0.1:12345

requests.get('http://example.org', proxies=proxies)
session.proxies.update(proxies)
```



# Auto Retry

> `reqeusts` uses `urllib3.util.retry`
>
> ref: [urllib3](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#utilities)



```python
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter

s = Session()
retries = Retry(
    total=3,
    backoff_factor=0.1,
    status_forcelist=[502, 503, 504],
    allowed_methods={'POST'},
)
s.mount('https://', HTTPAdapter(max_retries=retries))
```



# Timeout

- `timeout=5  # 5 seconds`
- `timeout=(5, 30)  # 5s for connect, 30s for retrive`

# Blocking IO

requests is always blocking even using stream. 



