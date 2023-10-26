# Python-Learning

> What I will do with this repository: 
> 
> - [ ] Python basic usage (basic var types, define func & class, etc.);
> - [ ] Python advanced features (GIL, singleton, @decorator, etc.);
> - [ ] Powerful built-in modules (multiprocessing, re, threading, etc.);
> - [ ] Powerful third-party packages (asyncio, requests, selenium, etc.);

# TODO

- [ ] 对象有一个`__str__()`方法，打印的时候可以打印对应的**字符串**
- [ ] slice
- [ ] enumerate, zip
- [ ] range

# Basic Usage

## Token & Keyword, 标识符 & 关键字

- 标识符由字母、数字、下划线组成
- 不能以数字开头
- 区分大小写
- 以下划线开头的标识符是有特殊意义的。以单下划线开头 `_foo` 的代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用 `from xxx import \`* 而导入。 
- 以双下划线开头的 `__foo` 代表类的私有成员，以双下划线开头和结尾的 `__foo__` 代表 Python 里特殊方法专用的标识，如 `__init__()` 代表类的构造函数。

- 关键字不能用作常数或变数，或任何其他标识符名称
- 所有 Python 的关键字只包含小写字母。

## Annotation, 注释

- `#` 单行
- ` ```, """ ` 多行

## INDENT, 缩进

- python 最具特色的就是用缩进来写模块。
- 缩进的空白数量是可变的，但是所有代码块语句必须包含相同地缩进空白数量，这个必须严格执行。 
- 建议你在每个缩进层次使用 **单个制表符** 或 **两个空格** 或 **四个空格** , 切记不能混用

## Variable Types, 变量类型

### overall features, 通用特征

- `type(object), isinstance(object, type)`可用于判断类型

- mutable: list, set, dict
- immutable: number, tuple, string
- mutable 的对象，如果对对象做了修改，就是在原有内存地址上修改
- immutable对象的修改，实际上会在另一个内存地址上放置新的数据
- mutable和immutable是**十分具有特色的特征**，如果不注意这个特征，可能会带来意外的错误

### number

分成int, float, complex, bool, 但用起来没什么区别

### string

- **常用slice来截取一部分**
- `r""`可以避免转义
- str.count('a') 返回数量
- str.find(substr, beg, end) 可判断substr是否在str中，返回下标/-1
- str.index() 同上，但不返回-1，而是报错
- isnumeric, isalnum, islower, isdigit等
- strip 截掉空白字符
- replace(old, new)
- split(char), return [str]

### f-string

f-string的用法：

- 使用大括号替换资源`print(f"name = {name}")`
- **高效concat**
- 右对齐，`f'{x:>10}`，左对齐<，居中=
- 使用特殊字符占位，默认空格`f'{x:->10}'`
- 格式化浮点数，`f'{x:.2f}'`
- 转换进制，`f"{int:b}"`，b-2，o-8，x-16，X-16大写，c-ascii

### list (array)

> 据说底层是C的array，每个元素都是一个指针

- 可以容纳任何东西，但通常是储存同种类型的元素
- **常用slice, enumerate**
- list.append/extend()会在原有基础上增加
- 而 list + another list 会返回一个新的列表
- list.copy()返回一个shallow copy
- pop(), append(), count()
- list.reverse() 返回新列表
- list.sort() 原地修改，而global sorted() 返回新列表

### queue.Queue

我不喜欢用这个，建议用下面的collections.deque

### collections.deque

- 和list差不多，api基本一致，但是deque很方便
- pop, popleft, append, appendleft
- extend, extendleft


### tuple

- 和list差不多，但是immutable
- 不能修改，但可以连接生成新的tuple

### dict (Hashmap)

- key 必须是 immutable
- `dict[key] = value` 可以用来创建k-v
- `del dict[key]` 可以删除一个键
- 创建方法除了推导式，还有`dict = dict([ (k1,v1), (k2,v2) ])`
- 常用dict.keys(), values(), items()来遍历
- dict是有序的 (>= Python 3.7)
- dict传入的都是真实值，如下：

``` python
a = 1
b = a

dct = {a: 'value'}
print(dct[b])  # --> 'value'
print(dct[1])  # --> 'value'
```

### collections.Counter

Counter继承自dict类型，相当于是一种只用来计数的hashmap。以下是一部分常用操作：

- 可选的初始化：`c=Counter('ababc')`
- 查询：`c['a']`
- 修改：`c['a'] += 1`
- 删除：`del c['a']`
- 清空：`c.clear()`
- 总数：`c.total() == sum(c.values())`，values是dict的方法
- 合并两个Counter：`c.update(d), d is Counter`
- 减另一个Counter：`c.subtract(d)`
- 查询前若干个，未指定则按出现次数排序所有：`c.most_common(k)`
- 返回键的列表：`sorted(c)`
- 返回键重复值的次数的列表，如`c.elements() == list("aabbc")`

### collections.defaultdict



### set

- 无序的、不重复的、自动去重的序列；
- set.add(), update()
- remove()当元素不存在时会报错，discard()不报错
- pop() 随机弹出一个

## Comprehensions, 推导式

- list comprehensions: `[i*2 for i in range(5) if i%2]`
- dict comprehensions: `{i:i**2 for i in range(5) if i%2}`
- generator comprehensions: `(i**2 for i in range(5) if i%2)`

## Operator, 操作符

- `+-*, **`
- `/` 直接求除数
- `//`取整部分，`%`取余
- `:=` 边赋值边计算

---

| 学名 | 符号 | 解释                  |
|----|----|---------------------|
| 与  | &  | ab都为1则返回1，否则为0      |
| 或  | \| | 有一个为1，就返回1          |
| 异或 | ^  | ab不同则返回1，相同返回0      |
| 取反 | ~  | 按位取反                |
| 左移 | << | a<<3，左移三位，高位丢弃，低位补0 |
| 右移 | >> | 同上                  |

---

- `and, or, not`

---

- `a is b`用于判断内存地址是否一致
- `a == b` 判断值

---


| 运算符                      | 描述                                |
|--------------------------|-----------------------------------|
| **                       | 指数 (最高优先级)                        |
| ~ + -                    | 按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@) |
| * / % //                 | 乘，除，取模和取整除                        |
| + -                      | 加法减法                              |
| >> <<                    | 右移，左移运算符                          |
| &                        | 位 'AND'                           |
| ^\|                      | 位运算符                              |
| <= < > >=                | 比较运算符                             |
| <> == !=                 | 等于运算符                             |
| = %= /= //= -= += *= **= | 赋值运算符                             |
| is is not                | 身份运算符                             |
| in not in                | 成员运算符                             |
| not and or               | 逻辑运算符                             |

## Conditional Statement, 条件语句

- if, elif, else
- 条件判断是短路形式的，比如 `1>0 or 1/0` 是True, 即使第二个表达式计算不出来


## Loop Statement (for, while), 循环语句

``` python
for element in iterator: 
    statements

while x <= 10:
    statements
```

- continue, break 用于循环控制
- `while/for - else`用于正常结束循环的时候（break不算正常退出），额外执行的语句

## Function, 函数

### def func, 定义函数

``` python
def func(*args, **kwargs): 
    """
    description
    """

    statements
    return result
```

- 返回的值可以写多个，会自动封包成一个tuple
- 在声明函数使用参数时，可以标注参数类型，方便被调用：`def func(x: [int])` 建议传入一个整数列表

### lambda, 是匿名函数

``` python
func = lambda x: x+1
a = func(2)
a = (lambda x: x+1)(2)
```

### arguments, 参数

- 必备参数：就平时写的那种
- 关键字参数：使用关键字参数允许函数调用时参数的顺序与声明时不一致，因为 Python 解释器能够用参数名匹配参数值，在内部组装成dict
- 默认参数：**默认值必须是immutable**，**默认参数在定义时必须在最后面**
- 不定长参数：可以让函数处理额外的参数。
- 一个星号，导入的是tuple，常用`*args`
- 两个星号，导入的是dict，常用`**kw, **kwargs`
- ***星号的作用是对iterable的对象拆分元素，\*args = 1,2,3，对一个(args元组)拆分等于分散的元素***
- **在函数内不用写星号**
- **强制位置参数**：`def func(a, /, b, * c)`则星号后面的必须以关键字参数的形式传入，/ 之前的必须是不能是关键字参数，之间的随便

例子：假如我们要计算一些数的平方和，我们可以传入[1, 2, 3]，但是这不优雅，所以利用*args可以不组装成list。

``` python
def sq_sum(*args):
    s = 0
    for i in args:
        s += i * i
    return s

print(sq_sum(1,2,3,4,5,6,7,8,9,10))
```

### scope of arguments, 参数作用域

- 在函数里的某个参数，作用域是这个函数整体
- 内层嵌套函数可以调用外层函数的参数
- **函数想修改非函数部分的参数（想在局部空间使用全局变量），需要在函数内使用 global 关键字**

## Built-in PowerFuncs, 内置的高级函数

- map(func, iterable) -> map object(iterable), 返回一个映射
- functools.reduce(func(**2 args**), iterable), 返回一个结果；先计算前两个值，再将结果和第三个值相加
- filter(func, iterable) -> filter object(iterable), func(ele)为True的显示，为False的去掉
- itertools.accumulate(iterable, func(**2 args**)) -> accumulate obj, 返回一个累计值
- `sorted(iterable, key = [func[, reverse=True]])`, 默认从小到大，reverse控制方向，func控制比较的值
- list.sort() 和 sorted() 差不多，但是原地修改；sorted返回一个列表

``` python
from functools import reduce
from itertools import accumulate

a = [1, 3, 2, 5]
print(reduce(lambda x, y: x + y, a))
print(list(filter(lambda x: x % 2, a)))
print(list(accumulate(a, lambda x, y: 10 * x + y, )))

---
11
[1, 3, 5]
[1, 13, 132, 1325]
```

---

functools.partial(func, kw), 偏函数: 固定函数的某个值。

``` python
import functools

s = '1011'
int2 = functools.partial(int, base=2)
def int2_self(x): return int(x, base=2)

print(int(s, base=2))
print(int2(s))
print(int2_self(s))
```

## OOP, Object-Oriented Programming, Python面向对象

### Define Class and Create Instance, 定义类并且生成实例

- 通常类名要大写
- 所有Python的类，都继承自object

```python
class Student: 
    # __init__ 是初始化的函数，这里面都是properties
    # __init__ 的第一个参数必须是self，表示inst本身，并且调用的时候不用传递这个arg
    def __init__(self, name, number, age): 
        self.name = name
        self.number = number
        self.age = age
```

- 如果没有定义任何属性，则可以`alice = Student()`； 
- 如果定义了参数，则应当`alice = Student('Alice', 114514, 19)`;
- 应该在定义类的时候，将属性和方法都写出来。当然也可以在外部给一个inst增加未定义的属性，但是这样不安全，可读性差

### OOP Concepts, 面向对象编程的一些概念

和面向对象相对的是面向过程。如果采用面向对象的程序设计思想，我们首选思考的不是程序的执行流程，而是把数据被视为一个对象。

面向对象里最重要的就是Class和Instance。Class是抽象的模板，形容了一系列instance；而instance是一个个对象。

对象包括两大点：属性(attribute/property)和方法(method)。 
比如定义一个类student，“Alice”和“Bob”是这个类下的两个实例。在类中包括了属性：学号，身高，体重，年龄；还有方法（函数），比如吃饭，学习。

---

面向对象的几个特点：

- 数据封装，限制访问，继承和多态

---

#### Data Encapsulation, 数据封装

> “封装也称为信息隐藏,是利用抽象数据类型将数据和基于数据的操作封装在一起,使其构成一个不可分割的独立实体,数据被保护在抽象数据类型的内部,尽可能地隐藏内部的细节,只保留**一些对外接口**使之与外部发生联系。” 
> 
> 好处：
> 1. 控制存取属性值的语句来避免对数据的不合理的操作
> 2. 一个封装好的类，是非常容易使用的
> 3. 代码更加模块化，增强可读性
> 4. 隐藏类的实现细节，让使用者只能通过程序员规定的方法来访问数据

通过在class里定义一些方法（一些函数），来实现各种接口。比如定义打印年龄的函数：

``` python
    # 除了第一个参数是self外，其他和普通函数一样
    def print_age(self): 
        print(f"{self.name}的年龄是：{self.age}")
```

使用方法的方法：

``` python
alice.print_age()
```

---

#### Access Control, 限制访问

为了使得内部属性不被随意访问和修改（但是可以初始化），在创建类的属性时应这样：

```python
class Student(object): 
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
```

在Python中，实例的变量名如果以`__`开头，就变成了一个私有变量（private），只有内部可以访问，外部不能read。

- `__name__`这种是可以直接访问的特殊变量；
- `__name`这种是private变量；
- `_name`这种是在class中表示是公开的，但是不建议随意访问。*按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”。*
- 单下划线`_name`命名的变量（包括类，函数，普通变量）不能通过**from module import **导入到另外一个模块中。
- 双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。不能直接访问`__name`是因为Python解释器对外把`__name`变量改成了`_Student__name`，所以，仍然可以通过`_Student__name`来访问`__name`变量：`alice._Student__name`。但是不同版本的Python解释器可能会把`__name`改成不同的变量名。
- 如果我直接给私有变量赋值会怎么样呢？基于上一条，如果我在类外直接给`instance.__attr`赋值，其实会有两个属性：`__attr, _ClassName__attr`————后者才是我们想要的

上面的写法带来的问题：除了初始化，否则无法赋值；全程都无法读取

---

Java-like 的解决方案：通过定义 get 和 set 函数来解决问题：

- 副作用：顺便可以在 set 的时候校验参数一致性！

```python
class Student(object):
    def __init__(self, name, age):
        self.__grade = None
        self.name = name
        self.age = age

    def set_grade(self, num):
        self.__grade = num

    def print_age(self):
        print(f"{self.name}的年龄是：{self.age}")
```

---

Pythonic 的解决方案：使用 @property 和 @[attr].setter

```python
class Student(object):

    def __init__(self):
        self.__score = None

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, i):
        # check value
        if not isinstance(i, int):
            raise ValueError('int only, you fool')
        elif 0 <= i <= 100:
            pass
        else:
            raise ValueError('[0, 100] only, you fool')
        # set value
        self.__score = i


instA = Student()
instA.score = 76   # set score
print(instA.score) # get score
```

有几个要注意的点：

1. 必须先写`@property`把一个方法变成属性，才能写`@attr.setter`，调换顺序不行；而且应该是先把某个method变成attr了，接下来才能写`@attr.setter`，不同名是不行的；
2. 这里不用担心两个函数重复名字的问题，调用的时候都直接写属性名字就行（不该加下划线）；
3. 现在在外部可以和之前一样赋值和读取了
4. `@property`和`@*.setter`都写是可读写，如果只写第一个就是只读————可以用只读这个属性来实现一些需求
5. 假如是只读的，就不能给它赋值，包括在`__init__`里定义并初始化也不行
6. api和实例变量不能同名，否则解释器不知道是调用api还是变量名，就会无限递

#### Inheritance and Polymorphism, 继承与多态

**继承**：可以从一个父类、基类（base class）超类（**Super class**）创建子类（subclass）。

继承可以把父类的所有功能都直接拿过来，这样就不必重零做起，子类只需要新增自己特有的方法，也可以**把父类不适合的方法覆盖重写**。

继承什么？公有的属性和方法：

- 假如子类和父类都有同样名字的方法，子类的会覆盖父类的（多态）；
- 假如一个inst属于某个subclass，那他也属于base class；

```python
class Human:
    pass

class Student(Human):
    pass
# 学生单继承自人类
```

**多态**：指为不同数据类型的实体提供统一的接口，同一个行为具有多个不同表现形式或形态的能力。

多态存在的三个必要条件：

- 继承
- 重写
- ~~父类引用指向子类对象：**Parent p = new Child();**~~

![](https://www.runoob.com/wp-content/uploads/2013/12/2DAC601E-70D8-4B3C-86CC-7E4972FC2466.jpg)

在上图中，每个子类可以重写(override)父类的方法。

---

著名的“开闭”原则：

- 对扩展开放：允许新增`BaseClass`的子类；
- 对修改封闭：不需要修改依赖`BaseClass`类型的`draw()`等函数。

#### Duck Typing, 鸭子类型

> 鸭子类型（英语：duck typing）是动态类型的一种风格。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口，而是由"当前方法和属性的集合"决定。
>
> 当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。
>
> ——James Whitcomb Riley

Python这种动态语言不要求严格的继承，假如我新建一个class，不从animal继承，直接从object继承，再给他写一个run方法，那么也可以run。

我觉得都可以理解，因为是根据inst所在的class来找run的。只要这inst有run这个名字的方法，就都可以用。


## Exception, 异常处理





# Advanced Features

## Variables, Objects and Memory, 变量 - 对象 - 内存

- python中，万物皆对象。 
- python中不存在所谓的传值调用，一切传递的都是对象的引用，也可以认为是传址。
- 对于mutable: 类似C++的引用传递，将 a 真正的传过去，修改后fun外部的a也会受影响
- 对immutable: 类似C++的值传递，传递的只是a的值，没有影响a对象本身

``` python

def myfunc(t):
    t += 2
    print(id(t))


a = 1
print(id(a))
myfunc(a)
print(a)
print(id(a))
--------------------
2543723217136
2543723217168
1
2543723217136
# 因为 *不可变对象number* ，所以只传入了内存里的值；
# 可以看到a对应的地址没变，函数myfunc没有改变a对应的地址的内存里的内容，而是另外找了个地方
# 最后 a 对应的地址里面的内存内容还是 1 

-----------------------------------------------

def myfunc2(t):
    t.append('fuck')
    print(id(t))


b = [1, 2, 'a']
print(id(b))
print(myfunc2(b))
print(b)
print(id(b))
--------------------
2345014392832
2345014392832
None
[1, 2, 'a', 'fuck']
2345014392832
# 可以看到 *可变对象list* 所指的内存地址是不变的

```

还有一个特性，python为小int做了优化，有一个[-5, 256]的小整数池，在解释器启动的时候就创建了，可以避免频繁使用对象（假设频繁使用小整数）的创建和销毁。所有小整数对象都指向固定的地址。

``` python
a = 1
print(id(a))

b = 100
print(id(b))

b -= 99
print(id(b))
----------
1767367180528
1767367183696
1767367180528
```

## Closure & Decorator, 闭包和装饰器

## Multiple Inheritance & MRO, 多继承和继承顺序 

## Singleton in Python, 如何实现单例模式?

## Tail Recursion, 尾递归

通常的递归，会导致函数栈帧不断增加，直至达到最大限值——可能伴随着内存不足。Python 默认的最大递归深度为1000，但是可以手动修改。

一个递归的例子是求前n项正整数的和，或者乘积。

```python
def func(x):
    if x == 1:
        return x
    return x + func(x-1)
```

上面的例子意味着每一层栈帧都依赖于更上一层函数栈帧的计算结果。但是我们可以将这个函数优化成尾递归：函数返回值只由递归函数本身组成。

```python
def func(x, pre=0):
    if x == 1:
        return x+pre
    return func(x-1, x+pre)

print(func(5))  # --> 15
```

- 尽管如此，有些语言没有对尾递归做优化。
- Python/CPython解释器就没有优化，上一段的写法仍然会导致栈帧溢出。
- gcc -O2 级别的优化就会做优化

[以下内容在参考内容的基础上做了一点改进：](https://www.jb51.net/article/247073.htm)

``` python
import sys


# 一个异常，用于传递参数
class TailRecursionError(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_rec_opt(func):
    def _opt_exec(*args, **kwargs):
        f = sys._getframe()

        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecursionError(args, kwargs)

        while True:
            try:
                return func(*args, *kwargs)
            except TailRecursionError as e:
                args = e.args
                kwargs = e.kwargs

    return _opt_exec


# 一个递归函数，尾递归形式，用于计算1+2+...n的和
@tail_rec_opt
def recursion(n, pre=0):
    if n == 1:
        return pre + 1
    else:
        return recursion(n - 1, pre + n)


print(recursion(5))
```

- 尾递归实际上，是在装饰器里的while循环里完成的

在执行的过程中，首先栈帧会变成下面的样子：

| 层数编号 | 栈帧函数            | 要求返回值             |
|------|-----------------|-------------------|
| 4    | _opt_exec(4, 5) |                   |
| 3    | func(5, 0)      | opt_exec(4, 5)    |
| 2    | _opt_exec(5, 0) | return func(5, 0) |
| 1    | module          | -                 |

- 此时帧4会触发异常，因为和帧2的函数名一样。此时会结束函数调用，销毁帧4，并且返回一次递归函数计算的结果：`e(4, 5)`
- 此时异常会向下返回，直至回到帧2的return部分
- return的异常将被try-except捕捉，并修改帧2中的args和kwargs

此时将变成：

| 层数编号 | 栈帧函数            | 要求返回值             |
|------|-----------------|-------------------|
| 2    | _opt_exec(4, 5) | return func(4, 5) |
| 1    | module          | -                 |

并继续运算，变成：

| 层数编号 | 栈帧函数            | 要求返回值             |
|------|-----------------|-------------------|
| 4    | _opt_exec(3, 4) |                   |
| 3    | func(4, 5)      | opt_exec(3, 4)    |
| 2    | _opt_exec(4, 5) | return func(4, 5) |
| 1    | module          | -                 |

继续运行循环，直至：

| 层数编号 | 栈帧函数             | 要求返回值              |
|------|------------------|--------------------|
| 3    | func(1, 14)      |                    |
| 2    | _opt_exec(1, 14) | return func(1, 14) |
| 1    | module           | -                  |

这次帧3直接返回了15，因此整个函数返回了15，递归结束。





# Built-in Packages & Modules

# Third-Party packages & Modules









