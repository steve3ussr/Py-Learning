# threading

> A high-level module based on `_thread` module. 



## Thread Object

普通构造方法: `threading.Thread(target=func, args=tuple)`

普通运行方法: `threading.start()`

---

可以创建一个子类, 并且自定义线程对象, **但建议至多重载两个函数: `__init__`和`run`**. 其中: 

- 重载构造器时应当首先运行`super().__init__()`,  然后再运行其他内容
- 目前不知道重载`run`有什么用

---

- `Thread.daemon` 是一个flag
- `Thread.is_alive`判断`run`是否结束



## Daemon Thread

> - `daemon_terminate_ways.py`: show abrupt / graceful way when daemons quit
> - `daemon_user_main.py`: 展示了`daemon`会在主线程退出前自动退出; 主线程会阻塞等待`user`线程结束后再结束

在Unix中, `daemon`通常指一种服务型的进程/线程, 一旦被创建, 就会一直在后台运行, 并且为前台应用提供服务: 例如邮件定时收件, 处理web请求, 连接的keep alive, 打印请求处理, 线程池中的`workers`, etc. 通常`daemon`的调度优先级比较低, 因为他们是在后台提供服务的. 

与`daemon`相对的被称为`non-daemon`或者`user`, 这些是与用户交互的前台. 

通常`daemon`是一个"孤儿进程", 其父进程为`init`, 并且没有任何输入输出, 不与任何tty相关. 

---

在Python中, 一个程序有主线程, 并且他可能还有一些`user`或者`daemon`线程. 下面有这些种可能: 

- 全都是`user`线程: 如果主线程运行结束了, 并不会退出, 而是自动等待所有`user`线程结束后再退出 (是的, 甚至不需要`join()`). 可以认为`user`线程会自动阻塞主线程; 
- 全都是`daemon`线程: 如果主线程运行结束了, 就会终止所有`daemon`线程, 然后结束主线程. 既然没有`user`线程, 那就不需要`daemon`提供服务了; 
- 两种线程都有: 先等待`user`线程结束, 然后再终止`daemon`和主线程. 

`daemon`的**意义**在于默默地在后台运行; 主应用程序退出后, 可以自动退出的一些操作. 这当然很好, 但也会带来一些问题. 假如`daemon`线程退出时还拥有DB, file等资源, 不释放资源可能会出现问题. 如果希望`daemon`线程可以**优雅地退出**, 应当让他们成为`non-daemon`的, 并且通过`Event`作为信号通知这些线程结束. 





## Thread Pool

`threading`并不提供线程池, 可用的线程池包括: 

- `concurrent.futures.ThreadPoolExecutor`
- `multiprocessing.pool.ThreadPool`



## Thread Run Exceptions

> `except_hook.py`

可以重载一个异常捕捉函数: `threading.excepthook`, 用于捕捉`Thread.run()`中未捕获的异常. 

**不要储存`thread`, 否则可能会复活. **



## Lock, RLock

原理很简单, 但写出死锁也很简单。



## Condition

除了`acquire`和`release`，`wait / wait_for`可以释放锁并阻塞，直到有人`notify / notify_all`后才能唤醒。



## Semaphore

semaphore的主要用途是保护有限的资源，semaphore variable作为资源数量上限供所有线程同步。

- `acquire`将会使得内部计数器-1 / 阻塞直到有人`release`；
- `release`使得内部计数器+1
- `BoundarySemaphore`更高级，能避免`release`次数过多导致计数器值变高；



## Event

Event像一个flag，不用`acquire`和`release`，而是`set, clear`改变状态, `is_set`查询状态, `wait`阻塞并等待`True`。



## Timer

> `recycle_timer.py`

是`Thread`的子类，休眠`interval`后执行`target`，同样用`start`启动. 



## Barrier

设定线程数量，如果这些线程都await并且阻塞，就自动放开栅栏让这些线程恢复工作；可用于线程间同步数据。
