# TCP/UDP Server-Client Project (Based on python socket)

> 基于 Python socket 的 TCP/UDP 客户端-服务端

## 1 Simple client - server

> `client.py`
>
> `server_single.py`

为了学习使用，将服务端地址固定设置为`127.0.0.1:13000`。

### client (cli)

- 设置`Client().socket`为客户端通信socket
- `_connect()` method: 尝试连接至server
- `_exec()` method: 主要功能，向server发送字符串并回显；当且仅当输入`quit`时主动关闭client
- `start()` method: connect and exec，并且捕捉连接异常（如服务端主动关闭）
- 为了避免粘包，在`input()`后加一个EOF

### server (svr)

- 设置`Server().socket`，并绑定到`127.0.0.1:3000`
- 开始监听
- `_convert()` method: 实现字符串转换
- `_exec()` method: **主要方法，循环：阻塞等待accept - 与 cli 互动 - 关闭连接**；与cli的互动包括：循环：接受信息 - 转换 - 回报，直到接受信息为`quit`
- `start()`当`exec()`异常退出后再次启动；捕捉异常主要为cli主动关闭导致。

## 2 Mock Concurrent Client

> `client_mock.py`
>
> `mock_multi_client_async.py`
>
> `mock_multi_client_thread.py`

为了模拟并发情况，首先需要改造客户端。从Client继承一个ClientMock，主要作用是：通过传入一个Task tuple of `(interval, message)` 自动通信。

为了创建多个客户端，通过asyncio/多线程模拟多个客户端的并发。client alias, task (interval, message)都通过列表生成，同时生成cli list (此时并未启动)

### Mock by Asyncio (not good)

在一个TaskGroup中启动所有cli，但由于cli是阻塞的 (含有time.sleep)，所以通过`asyncio.to_thread`发送到其他线程。

**该方法存在问题，asyncio根据资源自动调度并行的task；如果我设置了100 cli并发，实际可能只有20个并行数**

### Mock by Thread Pool

这里可以用普通的`threading.Thread(target=cli_start_func, args=(cli_obj, ))`，然后直接start，不join，但这样不方便跟踪客户端结束时间；所以最好是用池化方法，自动同时join。

- threading模块竟然没有线程池。
- 使用`concurrent.futures.ThreadPoolExecutor`
- 使用`multiprocessing.pool.ThreadPool`
- 使用`multiprocessing.Pool`，用进程池

以上线程池/进程池的性能还不清楚。



## 3 Server for Multi Connect by Asyncio

> `server_multi_async.py`

相比于使用socket这一低等级API，asyncio.stream提供了若干高级API。

- `coro: asyncio.start_server(client_connect_cb, host, port[, ...])`可以启动一个服务端，其中：
  - cb: callback，当新client连接established之后call；可以是普通callable函数/coro函数，如果是coro函数，auto scheduled as A TASK when called；
  - cb必须接受两个参数：reader和writer，它们分别是StreamReader和StreamWriter的实例；这两个类都**不推荐手动实例化，建议只通过`asyncio.stream`的高级API返回（`open_connection, start_server`）**
  - reader基本只要read方法，还有额外的参数用于限制buffer大小
  - writer除了write方法，还**必须**通过`await writer.drain()`确保数据能写入IO buffer。如果buffer达到上限，就会阻塞；
  - `writer.close()`**可以关闭asyncio.stream以及下层的socket**，建议和`await writer.wait closed()`一起使用
- `server.serve_forever()`启动服务端，除非main coro被取消；每个Server对象只应该启动一次该方法。

该处还有一个问题，stream reader识别EOF作为结束，所以在client中input后加了EOF作为分割。

相比于最初的server，callback/handler只需要处理单次连接的内容：循环等待cli输入，处理异常，关闭连接。



## 4 Server for Multi Connect by threading

> 传统，可靠。
>
> `server_multi_thread.py`

主server绑定端口、建立监听后，任何从accept获得的 client socket 以及 client addr都会被发送到新线程上处理：`cli_thread = threading.Thread(target=handler, args=(client_socket, addr))`。

handler的功能和使用asyncio的一样。









