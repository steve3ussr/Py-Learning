> 参考文献
>
> [【python】asyncio的理解与入门，搞不明白协程？看这个视频就够了](https://www.bilibili.com/video/BV1oa411b7c9)
>
> [Python 3.12.3 asyncio](https://docs.python.org/3/library/asyncio.html)
>
> [Python 3.12.3 Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
>
> 

# 如何理解异步框架Asyncio？

## 异步是什么？

假如我现在需要从互联网上下载10张图片，但是每张图片需要20s才能下载完成（不考虑双方带宽资源限制的情况下）。

在同步/Synchronize模式下，这需要大约200s才能完成——我等待上一张图片下载完成，然后再开始下载下一张图片。

但其实我们没必要等待下载完成。我可以在一张图片下载过程中，再去下载其他的图片。不考虑资源限制的话，我可以同时下载所有图片，这样一共需要大约20s就能完成所有任务，我节约了等待的时间。

**这就是异步的最大作用。**异步，在计算机编程中，是指独立于主程序流程的事件发生以及处理此类事件的方式。这些可能是“外部”事件，例如信号的到达，或由程序发起的与程序执行同时发生的操作，而程序**不会阻塞等待结果**。

异步编程技术一般用于IO bound task（而不是CPU bound）。

## Asyncio如何工作？

异步的核心是一个分配任务的核心，它可以正确地处理一大堆任务。在Asyncio中，这个核心被称作 Event Loop，他负责调度所有任务的运行。在简单应用中，我们不需要关心调度细节，只需要创建任务，并告诉Event Loop开始执行这些任务。

## 什么是“任务”？

在Asyncio中，所谓的任务有两种表达方式，一种是Coroutine/Coro/协程，一种是Task/任务。

当我们提到Coroutine时，它可以指一个定义——通过书写一个coroutine function来定义一个任务，例如：

```python
import asyncio

async def func(s):
    print(f"{s} start... ")
    await asyncio.sleep(5)
    print(f"{s} end. ")
```

当执行函数时，函数返回一个Coroutine object，而不是生成一个我们期待的结果，也没有经过Event Loop的调度和执行。

Task是Event Loop调度的对象。创建Task需要首先封装一个Coroutine，然后才能被执行。当一个Task被创建的时候，他**将自动地被Event Loop安排计划执行（不是立即执行，而是 be scheduled）**。

## Ecent Loop如何调度控制权？

Event Loop轮询所有的Task，发现可以执行的Task就执行。

当然，tasks之间可能存在依赖关系。例如Task1运行中要求必须得到Task2的运行结果，否则就不能继续；这时控制权将从Task1返回Event Loop，并由Event Loop选择下一个可执行的任务；直到Task2执行完成之后，Event Loop才有可能继续执行Task1。

以上暗含一个事实，即Event Loop不能强行从Tasks手中夺回控制权，除非Tasks主动交出控制权。在以下两种情况下，Task会主动交出控制权：

1. Task中要求另一个Task先完成（await Task）
2. Task运行结束

## 什么是“await”和“awaitable”？

`await`关键字只能被用于coroutine function中，可以挂起一个任务（并等待另一个任务，建立依赖关系），交出当前coroutine/task的控制权。`await`关键字后面必须接着一个awaitable对象。

awaitable对象（常常被简写为aw，aws），可以是coroutine对象、Task对象、Future对象—以及任何包括`__await__()`函数的对象。

- coro对象：未被计划执行
- Task对象：已经被计划执行
- Future对象：一个异步操作的结果，例如一系列Tasks

==`await`还有这样的特性：如果`await`一个Coro，他会自动转化成一个Task，同时自动计划执行。而如果`await`一个Task，他会等待这个Task结束。可以认为，一个coro被`await`了才能确保其中的语句被真正执行完毕。==

- 如果coro没有被`await`，会给出warning；
- 如果coro被重复`await`，会报错：`RuntimeError: coroutine is being awaited already`

## 什么是协程？

协程也叫微线程，是一个更加轻量级的资源调度方式。计算机分配资源的最小单位是进程，进程中至少包括一个线程。即使是最小的线程，在执行时也需要在用户态和内核态之间来回切换，而协程只需要在用户态之间切换上下文。

[协程与线程](https://en.wikipedia.org/wiki/Thread_(computing))非常相似。然而，协程是[协作式多任务处理](https://en.wikipedia.org/wiki/Cooperative_multitasking)，而线程通常是[抢占式多任务处理](https://en.wikipedia.org/wiki/Preemption_(computing))（存在竞争冒险问题）。协程提供[并发性](https://en.wikipedia.org/wiki/Concurrency_(computer_science))，因为它们允许任务无序或以可更改的顺序执行，而不改变总体结果，但它们不提供[并行性](https://en.wikipedia.org/wiki/Parallel_computing)，因为它们不会同时执行多个任务。协程相对于线程的优点是它们可以在[硬实时](https://en.wikipedia.org/wiki/Hard_realtime)上下文中使用（协程之间的[切换](https://en.wikipedia.org/wiki/Context_switch)不需要涉及任何[系统调用](https://en.wikipedia.org/wiki/System_calls)或任何[阻塞](https://en.wikipedia.org/wiki/Blocking_(computing))调用），不需要同步原语，例如[互斥体](https://en.wikipedia.org/wiki/Mutex)、信号量等。为了保护[关键部分](https://en.wikipedia.org/wiki/Critical_sections)，并且不需要操作系统的支持。

可以使用抢占式调度线程来实现协程，这种方式对调用代码来说是透明的，但是一些优点（特别是硬实时操作的适用性以及它们之间切换的相对便宜性）将会丢失。

# 一个简单的例子

> 从一个简单的例子入手，了解如何使用asyncio异步编程
>
> basic_n_coros.py

## 定义coro

假设我有一个IO bound操作（可能是DB或者net），需要一段时间才能得到响应。可以用sleep来模拟操作，如下面这个coroutine function所示：

```python
async def func(s):
    begin = time.time()
    print(f"{s} start... {time.strftime('%X')}")

    await asyncio.sleep(5)

    end = time.time()
    print(f"{s} end.     {time.strftime('%X')} --- {end-begin:.2f}s elapsed.")
```

1. `async def`表示这是一个协程函数；
2. 这里的sleep并不是常见的`time.sleep()`，因为这是一个阻塞线程的函数；而`asyncio.sleep()`是非阻塞的；包括其他类型的操作（网络操作，文件操作，etc.）都必须使用非阻塞的函数。对于网络操作可以使用`aiohttp`库，对于文件操作可以使用`aiofile`库。
3. 为了更好地观察一个协程的运行情况，用了`time.strftime('%X')`，它会返回一个`hh:mm:ss`形式的字符串

## 初次运行coro

`asyncio.run(coro)`是常用的函数，总是会创建一个新的Event Loop并在结束时关闭之。它应当被用作 asyncio 程序的主入口点，理想情况下应当只被调用一次。

```python
async def func(s):
    begin = time.time()
    print(f"{s} start... {time.strftime('%X')}")

    await asyncio.sleep(5)

    end = time.time()
    print(f"{s} end.     {time.strftime('%X')} --- {end-begin:.2f}s elapsed.")


if __name__ == '__main__':
    asyncio.run(func('coro1'))
```

当我运行这个程序时，屏幕上正确地显示了：

```
t1 start... 15:33:35
t1 end.     15:33:40 --- 5.01s elapsed.
```

## 增加更多aws

只运行一个coro还是不能实现目标，因为我们希望同时进行多个耗时的操作。可以用一个主函数来创建多个Coros/Tasks（或者直接说aws）：

```python
async def main():
    await func('coro1')
    await func('coro2')
    
asyncio.run(main())
```

但结果和预期的大相径庭：

```
coro1 start... 15:41:28
coro1 end.     15:41:33 --- 5.01s elapsed.
coro2 start... 15:41:33
coro2 end.     15:41:38 --- 5.00s elapsed.
```

这两个任务并没有并行地等待，而是顺序执行；原因在于`await`：当运行到`await func('coro1')`的时候， `main()`交出控制权，暂时挂起，并且在Event Loop中建立一个依赖关系：必须等待`func('coro1')`这个Task完全结束，`main()`才能继续运行。

所以可以把`main()`它改写成：

```python
async def main():
    task1 = asyncio.create_task(func('coro1'))
    task2 = asyncio.create_task(func('coro2'))
    await task1
    await task2
```

1. 在使用`asyncio.create_task()`之后，这两个coros就被转化成Tasks，并且由Event Loop安排计划执行。此时Event Loop中有main、coro1和coro2三个Tasks，但当前仍然在执行main。
2. 当`main()`运行到`await task1`时，建立了一个依赖关系（main必须等待task1完成）；Event Loop将从task1和task2中选择一个来执行，假设执行的是task1。
3. 当task1运行到`await asyncio.sleep(5)`时，Event Loop将只能运行task2；
4. 当task2运行到`await asyncio.sleep(5)`时，Event Loop将等待任何一个可执行的任务；
5. task1的sleep结束了并通知Event Loop，因此task1继续执行直至结束；
6. Event Loop发现此时task2的sleep也结束了，可以执行；main的`await task1`也结束了，可以继续执行；假设Event Loop恢复执行main，则main要求等待task2完成；
7. task2的sleep完成，task2结束；
8. main继续执行，main结束

```
coro1 start... 15:49:38
coro2 start... 15:49:38
coro1 end.     15:49:43 --- 5.01s elapsed.
coro2 end.     15:49:43 --- 5.01s elapsed.
```

可以看到，现在两个coros可以并行等待了。

## 优雅地运行多个任务

### Asyncio.gather

如果只有两个任务，当然可以用手动创建两个任务。但如果我有更多的任务需要并发呢？显然不可能再手动创建任务了。

一种并发运行任务的方法是`asyncio.gather(*aws)`，例如：

```python
async def main():
    await asyncio.gather( *[func(f"coro_{i}") for i in range(10)] )
```

注意：

1. 需要将aws解包后传参
2. 如果aws中包括coro，将会自动封装为Task并计划执行

运行结果为：

```
coro1 start... 20:51:32
coro2 start... 20:51:32
coro3 start... 20:51:32
coro1 end.     20:51:37 --- 5.00s elapsed.
coro2 end.     20:51:37 --- 5.00s elapsed.
coro3 end.     20:51:37 --- 5.00s elapsed.
```

### Asyncio.TaskGroup

如果你使用的版本**大于等于Python3.11**，另一种方式是使用`asyncio.TaskGroup`，这是一个异步上下文管理器。***当该上下文管理器退出时所有任务都将被等待***。示例如下：

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        for i in range(1, 4):
            tg.create_task(func(f"coro{i}"))
            
if __name__ == '__main__':
    asyncio.run(main())
```

注意：

1. `asyncio.TaskGroup().create_task()`和`asyncio.create_task()`签名一样
2. `asyncio.TaskGroup().create_task()`后并没有被Event Loop调度执行，而是等到退出上下文后才被计划执行。

## 保留对任务的引用

通过`asyncio(.TaskGroup).create_task`后，需要保存一个对task的**强引用**。EventLoop将只保留对任务的弱引用， 未在其他地方被引用的任务可能在任何时候被GC，即使是在它被完成之前。

为了避免任务在执行过程中消失，请将tasks放到一个多项集中:

``` python
tasks = set()
for i in range(10):
    tasks.add(create_task(coro))
```



# 如何获取任务的返回值？

> basic_n_coros_with_returns.py

对于Task对象，通过Task.result()可获取返回值。

这更体现了上一个小节的重要性——应当保存对task对象的引用。通过遍历task对象的引用，可以获取他们的结果。

# 异常和取消

> task_cancel.py

Task对象可以通过task.cancel()被取消计划执行，此时该task会raise一个`asyncio.CancelledError`。

推荐在coro中包含异常处理情况，例如：

``` python
async def coro(args):
    try:
        pass
    except asyncio.CancelledError:
        pass
    	raise  # 可以raise，也可以不raise
    finally:
        pass
```

- 在gather中：一个task被取消，不会影响他对应的subtask
- 在Taskgroup中：当计划执行任务中的一个被取消后，相关的subtask的都会被取消



# 超时

> cm_timeout.py

有一个上下文管理器，asyncio.timeout(delay)：

- 如果delay为None就不会超时（也没有意义）；
- 如果设定为一个数字，那这个管理器内的所有task都应该在这个时间内完成，否则后续的task就会被取消
- 如果超时会raise CancelledError，但这个cm会自动转化为TimeoutError，所以**应该对cm捕捉TimeoutError**
- 可以先设置delay=None，在中途再增加delay（如果一开始还不确定延时是多少）。但注意：Event Loop有一个内部的时间戳，不等于time.time()，所以延迟时间应该是当前EventLoop的时间戳+我们期望的超时时间。**注意区别绝对时间和相对时间**

# 避免阻塞函数

> bypass_block.py

为了不阻塞，常规的time.sleep改成了asyncio.sleep，常规的http get变成了aiohttp等；但如果有些阻塞型IO操作没有人将其改为非阻塞的怎么办？

通过`asyncio.to_thread(func, args, kw)`可以将阻塞型函数发送到其他线程，这样就不会阻塞event loop所在的线程。

对于CPython解释器，这只能解决IO bound，换成其他解释器可以解决CPU bound。
