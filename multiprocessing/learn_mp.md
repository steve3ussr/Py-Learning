# Multiprocessing Basic





# 首次启动几个进程

> start_2_proc.py

- mp.Process是基本类型，生成新进程的时候就会创建一个该对象。
- Process的api和threading.Thread类似，通过start()启动。
- 通过join()可以阻塞当前进程，并等待调用join的Process运行完成/报错/到达预定的超时时间

# 查看进程信息，初探树状进程信息

> disp_proc_info.py

- 通过os获得pid和ppid
- 可以看到，手动定义的进程都是main的子进程，而main的进程还是另一个进程的子进程

这里有几个问题：

1. py程序运行的进程是什么样的？
2. 进程以哪种方式创建？
3. module name是什么意思？
4. 为什么官方文档强调多进程必须在main环境下运行？

## py运行的进程形式

在linux下通过pstree查看进程树，如下所示：

```
init(Debian)─┬─...─┬─...
             │     ├─...
             │     ├─node─┬─bash───python3───python3───sh───pstree
             │     │     
             │     │      
             │     └─...
             ├─...

```

在windows下通过os.getpid获取pid后，使用`psutil.Process(id).name()`获取名字，如下所示：

```
# disp_proc_info_win.py

5532 --> 17452
5532: pycharm64.exe
17452: python.exe
```

可见main进程是调用者的子进程，不管是bash还是pycharm



## 进程的创建方式

根据官方文档：

- windows和macOS下通过spawn系统调用创建，启动新的Python Interpreter，父进程的数据等拷贝到子进程空间内，需要重新加载一遍父进程的包，因此启动较慢；但由于数据都是自己的，安全性较高
- Linux使用fork，继承父进程的数据和堆栈，fork了父进程的解释器

## 如何手动指定spawn和fork

在`__main___`环境下，调用一次`set_start_method('spawn/fork')`

## 为什么强调运行在main module下？

假设有一个程序：

```
# exec.py

import ...
func()

if __name__ == '__main__':
	foo()
```

当这个程序作为主程序运行时：

- 当前模块的`__name__`就是`__main__`，可以认为这是整个程序的全局环境
- 首先执行import 和 func
- 如果确认当前模块就是最高的环境，才会执行foo

当这个程序作为一个模块被调用时：

- 当前模块的`__name__`是`exec`
- 依然执行import 和 func
- 不会执行foo

---

假设现在有两个这样的程序：

```python
# only_main_exec.py
import only_main_lib as lib
lib.foo()

# only_main_lib.py
import multiprocessing as mp

class MyProc(mp.Process):
    def run(self): print('this is my proc')

def foo():
    p = MyProc()
    p.start()

```

- 如果通过spawn创建新进程：
  - 会重新导入`__main__`模块，也就是在新进程里重新执行`only_main_exec.py`；
  - 再次执行`lib.foo()`
  - 再次通过spawn创建新进程
  - 此时，不管是哪个进程，他的`lib.foo()`都没执行完，该进程的函数堆栈里都有这个函数

此时的进程树应该是：

```
cmd.exe -- py -- py -- py -- py --...
```

每个进程的函数栈都是：

```
MyProc
lib.foo
<module>, only_main_exec
every proc
```

---

- 如果通过fork创建新进程：

  - 不再重新导入并执行，fork父进程的函数堆栈
  - 可以正常运行

此时的进程树：

```
bash - py - py  
```

  此时的函数栈：

```

                           MyProc.run
MyProc                     MyProc 
lib.foo                    lib.foo
<module>, only_main_exec   <module>, only_main_exec  
Parent Proc                Child Proc initial
```

所以子进程会正常执行MyProc.run，然后退出

---

在使用spawn的时候，必须保证创建进程的函数只被导入一次，所以唯一的方法是放在`if __name__ == '__main__'`下，这是唯一能标记父进程和子进程区别的地方。

# IPC: Queue

> ipc_queue.py

`mp.Queue`和`queue.Queue`差不多，可以用于多进程之间共享信息，适合于n消费者和n生产者。

基本方法是get和put。他们的api相同，都包括：

- block=True: 默认值，如果队列已满/队列为空的时候会保持阻塞，并等待可以操作
- timeout=None: 默认值，最大阻塞多久

还有full，empty，qsize（大概数量）等。

---

值得注意的是：

1. 如果有多个进程同时将对象放入队列，那么在队列的另一端接受到的对象可能是无序的（在示例中可证明这一点）；
2. 由同一个进程放入的多个对象的顺序在另一端输出时总是一样的；
3. 如果一个进程在尝试使用 [`Queue`](https://docs.python.org/zh-cn/3.11/library/multiprocessing.html#multiprocessing.Queue) 期间被 [`Process.terminate()`](https://docs.python.org/zh-cn/3.11/library/multiprocessing.html#multiprocessing.Process.terminate) 或 [`os.kill()`](https://docs.python.org/zh-cn/3.11/library/os.html#os.kill) 调用终止了，那么队列中的数据很可能被破坏。 这可能导致其他进程在尝试使用该队列时发生异常。
4. queue是线程和进程安全的，但由于进程和线程调度顺序导致结果无序；对queue的操作都是原子的。

如果想保持顺序，可以传入tup(id, item)或者直接mp.Pool.map



# IPC: Pipe

> ipc_pipe.py

默认创建双工管道，返回两个connection对象，基本用法是send和recv。值得注意的是：

1. 多个进程同时使用send或同时使用recv可能导致数据损坏
2. 同时使用两端没有问题
3. 两个conn对象并不区分只能用于send或者recv
4. 不能传递太大的东西（32MB）
5. 如果没有东西可被接受，就会一直block

# IPC: Synchronization

> ipc_sync.py

如果多个进程或线程同时**非原子地**操作同一个**共享资源**，那么最好给他们加上锁。

例如，`a += 1`不是原子的，他可以分成几部分：

1. 读取a的值到寄存器
2. 寄存器自增
3. 把寄存器的值写到a

```python
import dis
def func(a):
    a += 1
print(dis.dis(func))
```

```
  5           0 LOAD_FAST                0 (a)
              2 LOAD_CONST               1 (1)
              4 INPLACE_ADD
              6 STORE_FAST               0 (a)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
```

## Lock, RLock

除了Lock，还有RLock，可重入锁。如果一个线程/进程想获取两次锁，再释放两次，使用Lock会导致死锁，使用RLock就没问题。

但是使用RLock也是，获取多少次就要释放多少次。



# 共享状态: shared memories (Value and Array)

> shared_mem.py

- pros：快
- cons：**限制比较大**，value和array都是ctypes对象。

Value:

- `a = Value('type', value)`
- 通过`a.value`获取
- type中，例如d代表double，i代表int

Array：

- `a = Array('type', iterable)`
- 通过`a[0], a[:]`获取



# 共享状态: server process

> shared_manager.py

mp.Manager()控制一个服务进程，服务进程的管理器可以包含多种Python对象。

管理器控制对象，对外提供的是Proxy Type，例如`mp.Manager().list([...])`是一个`ListProxy`。

值得注意的是：

1. 如果被管理的对象包含了普通 [`list`](https://docs.python.org/zh-cn/3.11/library/stdtypes.html#list) 或 [`dict`](https://docs.python.org/zh-cn/3.11/library/stdtypes.html#dict) 对象，对这些内部可变对象的修改不会通过管理器传播，因为代理无法得知被包含的值什么时候被修改了（代理只知道被管理对象的内存地址）；
2. 这个包含list或dict不仅限于字面意思，只要包含他们的数据类型都可能出现这种情况，例如自定义类的属性；
3. 但是把值直接存放在容器代理中，是会通过管理器传播的（会触发代理对象中的 `__setitem__` ）从而有效修改这些对象，所以可以把修改过的值重新赋值给容器代理。
4. 在示例代码中有一个这样的例子。我建议不管什么时候都用显式的存储。



# 生产者-消费者模型

> PCP: Producer-Consumer Pattern
>
> PCP_1to1 / Nto1 / 1toN / NtoN.py

- web服务器可以用，一些线程用来保持连接，另一些用来处理请求
- 消息队列可以用，尤其是在分布式里的异步通信
- 实时数据处理可以用，通过消息队列或者共享数据

## 1 to 1: a Minimal Realization

- 用一个mp.Queue作为数据队列
- consumer的终止是通过计数器实现的

## N to 1

- 将producer改为pool.map
- **简单更改会报错：**`Queue/Lock objects should only be shared between processes through inheritance`
- Queue是在main进程定义的，由两个子进程（producer和conmsumer）共享，但不能被子进程的子进程共享；Lock也是这样
- 将mp.Queue改为mp.Manager().Queue可以共享，Lock也是一样

## 1 to N

- 这时候会发现，cnt Value也必须改为manager的类型，否则无法在子子进程里共享
- 同时**cnt的读写必须加锁**，否则会出问题
-  但这个写法是有很多问题的，具体原因将在下面介绍。

## N to N

综合以上的代码，结果出现了问题。

```python
def _consumer(tup):
    l, q, cnt, ma = tup
    while cnt.value < ma.value:
        item = q.get()
        with l:
            cnt.value += 1
            print(f"{time.strftime('%M:%S')}      <-get-- {item}, {cnt.value}/{ma.value}")
        time.sleep(7)
```

1. while判断条件时用了cnt，所以循环的condition必须加锁
2. 判断条件和get这两句话不是原子的，所以有可能判断条件可以取，但该进程真正取的时候，queue已经被其他进程取干净了，该进程就会阻塞在get这一步，无法自动结束进程；
3. 在尝试纠错的时候，曾经给get加锁，结果导致了更严重的问题：如果一个进程持有锁，但是在get的时候阻塞了；其他进程不能获得锁，所以一整个锁住了。

如果是一个串行的consumer，我们会写成：

```python
def _consumer(tup):
    l_print, l_cnt, q, cnt, ma = tup
    while cnt.value < ma.value:
        item = q.get()
        cnt.value += 1
        print(f"<-get-- {item}")
        time.sleep(3)
```

在写的时候应该注意：

1. 循环条件应该放到循环体里，和其他cnt相关的共同加锁；
2. get和cnt+1必须是原子的；

修改后的应该为：

```python
def _consumer(tup):
    l_print, l_cnt, q, cnt, ma = tup
    while True:
        
        with l_cnt:
            if cnt.value >= ma.value: break
            item = q.get()
            cnt.value += 1
            
        with l_print:
        	print(f"<-get-- {item}")
            
        time.sleep(3)
```

# 序列化问题

- 在mp的默认实现中（例如mp.Queue, mp.Manager）下的基础都是Pipe，而Pipe就必须序列化后再传递。
- python默认用pickle库来序列化。
- pickle库有问题（pickle.dump），如果超过4G的对象就会序列化失败
