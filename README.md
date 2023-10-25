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
- 缩进的空白数量是可变的，但是所有代码块语句必须包含相同的缩进空白数量，这个必须严格执行。 
- 建议你在每个缩进层次使用 **单个制表符** 或 **两个空格** 或 **四个空格** , 切记不能混用

## Variable Types, 变量类型

### overall features, 通用特征

- `type(object), isinstance(object, type)`可用于判断类型

- mutable: list, set, dict
- immutable: number, tuple, string
- mutable 的对象，如果对对象做了修改，就是在原有内存地址上修改
- immutable对象的修改，实际上会在另一个内存地址上放置新的数据

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

### collections.deque

- 和list差不多，api基本一致，但是deque很方便
- pop, popleft, append, appendleft


### tuple

- 和list差不多，但是immutable
- 不能修改，但可以连接生成新的tuple

### dick (Hashmap)

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


# Advanced Features

## Variables, Objects and Memory

## Closure & Decorator

# Built-in Packages & Modules

# Third-Party packages & Modules









