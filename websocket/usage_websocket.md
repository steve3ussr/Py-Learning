# TODO

- [ ] auto keep alive to avoid timeout
- [ ] Encrypt: TLS
- [ ] 



# Background

WebSocket是一种应用层协议，提供了一种基于TCP的全双工协议。相对的，HTTP是一种半双工协议，典型的场景是客户端发起请求，而服务端响应请求 (request-response)。

在一些场景下，HTTP协议会不那么好用，比如多人在线游戏时，一个玩家移动到了另一个位置（通过向服务器发送一个移动位置的请求），而这个移动应该被同步到其他所有玩家。为了实现这一点，可以有以下几种方法：

1. 客户端每隔0.05s向服务器**轮询**一次，但这会消耗大量资源
2. 客户端向服务器**长轮询**，发送一个请求并设置一个较长的超时（比如120s）；当服务器发现没有任何数据可以推送时将不响应客户端请求，如果服务器有数据可推送才会响应请求。之后客户端继续发送请求并等待——相比于普通轮询，使用长轮询的确能降低一些资源消耗，但长轮询更适用于实时通讯等场景，在游戏中仍然需要非常高频率的请求。
3. Comet技术等

以上方法中，客户端为了获取服务器的推送仍然需要一条请求，一条包含推送的响应，这影响了带宽和网络延迟。从协议栈上来看：

| Layer       | Protocol | Duplex |
| ----------- | -------- | ------ |
| Application | HTTP     | *Half* |
| Session     | Socket   | Full   |
| Transport   | TCP      | Full   |

好好的全双工，都被HTTP的设计耽误成了半双工，因此WebSocket应运而生，提供了全双工的交互，并且性能消耗更低，更适用于实时的数据传输。

在很多方面，WebSocket和Socket的理念相同；但WebSocket更适合在浏览器中运行，直接基于Socket更适合在一般的桌面应用程序中使用。





# Basic C-S

## From Tutorial

> `./basic_c_s/server_start.py`

Note that: 

- serve will dispatch connections to handlers
- a future will stay in event loop, until an error is raised / a result is set; if nothing changed the future object, then the event loop will not stop
- when the handler return, serve will close the connection

> `./basic_c_s/client_start.py`

Note that: 

- using connect() object as cm will ensure itself closed properly



## Handle Exception: Close Connection, Timeout

> `./basic_c_s/server_forever.py, client_forever.py`

These c and s can run forever now, except for:

- connection will be closed when timeout, and a `ConnectionClosedError` will be raised
- connection can be closed at any side, and a `ConnectionClosedOK` will be raised 



## What is serve?

- 接受 handler, host, port
- 创建一个server coroutine, 监听host, port
- 当有一个客户端发起连接时, server将自动握手, 并委派给一个handler coroutine
- handler将接受一个connection (`ServerConnection inst`)
- 在任何情况下, 只要handler运行完成, server都将自动挥手, 关闭连接
- API 同 `asyncio.server`一样

推荐使用方法为cm, 这样可以确保退出:

```python
# Method 1
stop = asyncio.get_running_loop().create_future()
async with serve(handler, host, port):
    await stop        
    
# Method 2
server = await serve(handler, host, port)
await server.serve_forever()

# Method 3
async with serve(handler, 'localhost', 6789) as server:
    await server.serve_forever()
```



# Browser as Client

> websockets + HTML + js + WebBrowser
>
> - `shot_time.html`: load js
> - `show_time.js`:  载入时在DOM中body下插入ol (ordered list); 从websocket收到信息时, 新建li (list item), 插入文字, 再把li加入ol
> - `time_server.py`提供时间信息 
> - `time_server_regular.py`向所有客户端同步发送时间

值得注意的是：`time_server_regular`中没有让server serve forever，而是让`send_time`作为task一直运行。



# Use “Event” to Manage Clients

> - `counter.html/css`: load js 
> - `counter.js`: add event listener to element, send json when clicked, parse json when recved
> - `counter.py`: react to events

Note:

`async for`适用于处理IO iterator，例如网络或者文件；或者处理流式传输。`async for`类似于多个异步的consumer，而 async iterator类似于producer。

在`counter.py`中，不可能等待全部message都就绪后再处理，为了流式处理，可以：

1. 用async for来实现, 语法简单，因为有语法糖。
2. 用多线程实现，设置一个线程池，当出现msg时由线程池来消费，但这么写起来比较复杂

两种不同的处理方式的共同点是等待IO的时候并不会阻塞consumer，高效利用资源。

其中，async iterator需要有`__aiter__`，在本例子中的`websokcets.asyncio.ServerConnection`对象继承自`websockets.asyncio`中的`Conenction`对象，其`__aiter__`方法为：

```python
async def __aiter__(self) -> AsyncIterator[Data]:
    try:
        while True:
            yield await self.recv()
    except ConnectionClosedOK:
        return
```









# Quick Start: Connect4



## Basic Resources

> - `connect4.jss`: style
>
> - `connect4.js`: create board, check and play a move
>
> - `main.js`: call create board function
>
> - `index.html`: main ui
>
>   Note: this html can only be fully viewed by start a http server. Access it through file scheme will not load js because of CORS Policy: *Cross origin requests are only supported for protocol schemes: chrome, chrome-extension, chrome-untrusted, data, http, https, isolated-app.*





# Custom IRC

## Design

- [ ] 用户检测: 通过connection的remote addr判断IP, 相同IP的为同一个用户, 不再新增
- [ ] 维护用户dict, IP: 名字
- [ ] 最大用户数量限制: 10个
- [ ] 前端: text browser用于显示聊天信息
- [ ] 前端: text input用于输入消息
- [ ] 历史记录: IP: time, msg
- [ ] 历史记录最大限制: 1000条
- [ ] client发送消息给server
- [ ] server broadcast消息给所有当前连接的client



- 用户处理

  - 用户数量上限为20
  - 用户储存在`USER_DICT`中, 以ip为key, value中包括username和last login time
  - 建立连接时, 首先检测用户是否在`USER_DICT`中
    - 如果不在, 就先向客户端发送json, 请求set username, 并返回json格式的用户名
    - 如果在, 就active, 并把*conn*加入`USER_LIVE`
    - 发送系统广播, 通知用户进入, 用户数量
  - 断开连接前
    - 从`USER_LIVE`中删除
    - `USER_DICT[status]=0`
    - 发送系统广播, 通知用户离开, 用户数量

- 消息:

  - 加入deque
  - 

- main handler

  - 用户处理
  - 消息处理
  - finally 用户处理

- 消息: 系统广播

  - json type: `sys_broadcast`
  - msg: 用户加入/离开
  - value: 在线用户数量

- 消息: 用户消息

  - json type: `user_broadcast`
  - msg: 用户消息

- 前端

  - text browser
  - input dialog
  - send button
  - online cnt display

- 定时器

  - 定期储存msg list
  - 定期清理非活跃yong'hu

  

  





