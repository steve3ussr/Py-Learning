# TODO

- P56，2.7.4，似乎是改动的快排；
- P67，3.3.7，表达式转换；
- P130，11；BST和DST；
- P130，15；看了解析才会；
- P160~162，搜索算法；
- BST iter；

# 1 导论

## 1.4 Python基础

`range(a, b)`和`list[a:b]`差不多，都从a下标开始，但是不包括b下标。

# 2 算法分析

## 2.3 Python数据结构的性能

- `list = list  + [i]`比`list.append(i)`慢得多，连接比追加慢；
- `pop()`和`pop(i)`时间复杂度分别为1和n，即使是`pop(0)`也要慢很多；

![](https://i.imgur.com/rMbbmB7.png)

![](https://i.imgur.com/R5NNqpt.png)

# 3 基本数据结构

## 3.3 栈

- 栈具有反转特性；
- 在py里可以自定义一个类，用原生的list实现各种方法；
- ![](https://i.imgur.com/oIMIeme.png)

## 3.4 队列

- 和栈相反，先进先出，FIFO；
- 主要内容就是dequeue和enqueue；
- 可以用list实现；

![](https://i.imgur.com/RgCiE4I.png)

## 3.5 双端队列（deque）

- 像是stack和queue的结合，从两端都可以添加或者移除元素；
- add、remove和front、rear四种结合，以及查询个数和是否为空；
- 这里会涉及到`pop(0)`和`append(0, i)`，可以把这两种都放在前端，这样统一从后端比较快；

## 3.6.2 无序列表：链表

- 首先需要一个Node类，包括data和next两种属性；
- 重点在于Unorderlist类；
  - head用来保存head；
  - isEmpty看有没有节点；
  - add，添加到开头比较方便；
  - 遍历：
    - length
    - search
    - remove：需要双指针
    - append
    - insert
    - index
    - pop

### 3.6.3 有序列表

比如一些数字，它们会按照数字大小排列，而不是直接添加到开头——元素的位置取决于他们的特征。

# 4 Recursion

## 4.2 Introduction

**The Three Principles of Recursion**

以递归求数列的和为例：

1. 递归算法必须有基本情况（数列长度为1时返回）；
2. 递归算法必须改变其状态并向基本情况靠近（数列拆分为**首项**和**其余项**）；
3. 递归算法必须递归地调用自己（返回首项和**其余项的和**）。

## 4.3 Realization

递归通过**栈帧**来实现。

![](https://i.imgur.com/0gh20r1.png)

栈底部的将保留函数和使用的变量（局部变量作用域为该帧）；

栈顶计算的结果将一层层向下替换，直至栈空；

## 4.7 DP, GA

> DP: Dynamic Programming
>
> GA: Greedy Algorithm

例子：

有1、5、10、25美分的硬币，而我需要63美分，怎么才能让硬币数量最少呢？

GA：试图最大程度地解决问题，但这只是局部最优解。如果GA的话，需要2个25美分，1个10美分，3个1美分，暂时是全局最优；

但如果还有21美分的硬币，最优解是3个21美分硬币——这时候GA就不起作用了。

---

利用递归的思想：

> 1. 递归算法必须有基本情况（数列长度为1时返回）；
> 2. 递归算法必须改变其状态并向基本情况靠近（数列拆分为**首项**和**其余项**）；
> 3. 递归算法必须递归地调用自己（返回首项和**其余项的和**）。

1. 基本情况：当剩下的金额和某个硬币金额一样；
2. 多种靠近方式：
   1. 1美分+剩下的；
   2. 5美分+剩下的；
   3. 10美分+剩下的；
3. 递归：拆分成一个硬币剩下的金额；

> 但这有很大的问题：
>
> ![](https://i.imgur.com/yYDBYXJ.png)
>
> 重复调用的次数太多，比如16就出现了很多次

初始解法：

``` python
def calc_coins_recursion(self, val_list: list, charge: int):
    if charge in val_list:
        return 1
    else:
        return 1 + min(self.calc_coins_recursion(val_list, charge - x) for x in val_list if x < charge)
```

cache 解法，速度快了很多：

``` python
self.cache = dict()

def calc_coins_recursion_cache(self, val_list: list, charge: int):
    if _ := self.cache.get(charge):
        return _
    else:
        pass

    if charge in val_list:
        tmp = 1
    else:
        tmp = 1 + min(self.calc_coins_recursion_cache(val_list, charge - x) for x in val_list if x < charge)

    self.cache[charge] = tmp
    return tmp
```

dp解法：

``` python
    def dp_coins(self, val_list, change):
        # build
        for i in range(1, change+1):
            if i in val_list:
                self.dp[i] = 1
            else:
                self.dp[i] = min((self.dp[i-x] + 1 for x in val_list if x < i))

        return self.dp[change]
```

**DP是自下而上的，从初始值开始构建整个表格；虽然占用了一些空间用于储存，但是速度很快**

**递归是自上而下的，有可能会栈溢出**

# 5 Search & Sort

## 5.2 搜索

###  5.2.1 顺序搜索

在有序和无序列表中搜索元素，区别在于：有序的蕴含信息，超过某个元素后，剩下的元素也不可能是需要的元素。

### 5.2.2 二分搜索

> 前提：有序；
>
> 并且要考虑排序的成本有多高；

用两个 index 比 slice 要快，因为 slice 是 $O(n)$。

### 5.2.3 散列

> **核心：散列函数，处理冲突，再散列**

#### 散列，散列函数

散列中的每个位置被称为 Slot，假设是从 0 到 m-1 共 m 个；每个元素经过散列函数计算后得到介于 0 和 m-1 的数值，就可以插入槽——**因此第一个简单的想法就是取余**，对 m 取余。

> **尽管初始大小可以任意指定，但选用一个素数很重要，这样做可以尽可能地提高冲突处理算法的效率。**

$$
hash(x) = x \bmod m
$$

但这个函数不完美，如果两个数计算得到的余数一样，就会发生**冲突**；我们希望对不同的值进行运算能得到各不同的值——但**完美散列函数**并不存在。

- **折叠法：**比如有个电话号码，每3位成为一组，加起来（或者每隔一组数先反转一次，如256变成652再相加）得到一个数，然后再取余；
- **平方取中法：**先求元素的平方，取中间的几位数再取余；
- **如果是字符串：**可以用 ascii 值计算；为了避免 dog 和 god 这种异序词产生相同的值，还可以根据位置加上权重；

> 散列函数也不能太复杂，不然开销太大，有可能抵消$O(n)$的优势！

#### 冲突：接受不完美

假如还是之前的例子，77 会放在 Slot 0 里，但假如再来一个 55，就会出现冲突。

**[Open Addressing, Closed Hashing, 开放定址法](https://en.wikipedia.org/wiki/Open_addressing)**：

- **线性探测， Linear Probing：**冲突的时候，从头开始遍历；发现 Slot 1 是空的，就把 55 放进去；

![](https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/HASHTB12.svg/543px-HASHTB12.svg.png)

但这会产生**聚集现象**，如果一个槽发生太多冲突，线性探测会填满其附近的槽，而这会影响到后续插入的元素。

![](https://i.imgur.com/HqZcAtC.png)

为了避免聚集，可以不每次 +1，而是每次 +3；但这都是线性的：这就需要一个**再散列函数（Rehashing Function）**来计算新的 Slot 。

- **平方探测，Quadratic Probing：**

用二次函数计算：一开始 +1，后来 +4，然后 +9 ......

- **双重哈希，Double Hashing：**

用另一个 hash 计算。

- **链接法，Separate Chaining：**

把 Slot 改造成一个链表。

![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Hash_table_5_0_1_1_1_1_1_LL.svg/675px-Hash_table_5_0_1_1_1_1_1_LL.svg.png)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hash_table_5_0_1_1_1_1_0_LL.svg/750px-Hash_table_5_0_1_1_1_1_0_LL.svg.png)



#### 实现

> [Python 中 Dict 的实现](https://www.cnblogs.com/Xuuuuuu/p/13894009.html)

![](https://i.imgur.com/IpYEuWV.png)

![](https://i.imgur.com/QkNJM0i.png)

可以用两个列表实现，一对k-v有相同的index。



#### 时间复杂度，载荷因子

载荷因子：
$$
\lambda = \frac{\it{Elements\ \ Count}}{\it{Hash\ \ Table\ \ Size}}
$$
**载荷因子小，则不容易冲突；否则找到新的 slot 就更难，或者链表就更长。**

![](https://i.imgur.com/nVBxNei.png)



## 5.3 排序(Sorting Algorithm)

### 5.3.1 冒泡排序(Bubble Sort)

- 第一轮：对于前 `n-1` 个元素，比较他们和后一个的顺序；
- 第一轮结束后，最大/最小的元素已经在末尾了；
- 第 i 轮：对于前 `n-i` 个元素，比较；
- 到 n-1 轮结束后，还剩一个元素就在他应该的位置上；
- $O(n^2)$。

![](https://i.imgur.com/StaTFm9.png)

**改进方法：如果某一轮时，没有进行交换，说明可以提前结束。**

### 5.3.2 选择排序(Selection Sort)

1. 遍历全部，把最大的放在最后；
2. 遍历前 `n-1` 个，把最大的放在 `n-1` 的位置；
3. ......
4. 遍历前两个。

**选择排序的时间复杂度仍然是**$O(n^2)$，因为找到最大的值的索引这仍然是个$O(n)$的问题。

但是交换的次数相比冒泡排序要少。



### 5.3.3 插入排序(Insetion Sort)

在列表较低的一端维护一个有序的子列表，并逐个将每个新元素“插入”这个子列表。

**时间复杂度仍然是**$O(n^2)$。

> 这里的插入涉及到元素位置的移动（实质上为赋值），比交换要快：
>
> 移动操作和交换操作有一个重要的不同点。总体来说，**交换操作的处理时间大约是移动操作的3倍**，因为后者只需进行一次赋值。在基准测试中，插入排序算法的性能很不错。

![](https://i.imgur.com/UfMZtmQ.png)

![](https://i.imgur.com/gVDT37p.png)





### 5.3.4 希尔排序(Shell Sort)

> 基本排序算法中的插入排序虽然逻辑较为简单，但当排序规模较大时，经常需要将元素一位一位地从一端移动到另一端，效率非常低。于是Donald Shell设计了一种基于插入排序的改进版排序算法，故被命名为 Shell Sort。

希尔排序也称“递减增量排序”，它对插入排序做了改进，将列表分成数个子列表，并对每
一个子列表应用插入排序。如何切分列表是希尔排序的关键——并不是连续切分，而是使用增量
i（有时称作步长）选取所有间隔为 i 的元素组成子列表。

> 其中一个通项公式，可根据数据规模计算各项步长。


$$
\mathrm{step}( \mathrm{n} ) = \frac{1}{2}(3^\mathrm{n}-1), (\mathrm{n} \ge 1)
$$

![](https://i.imgur.com/w3lu4cX.png)

**尽管此时并不能说是完全有序，但是又前进了一步。**

接下来减小增量，直到最后增量为1，相当于一次普通的 Insertion Sort 。

**希尔排序的时间复杂度大概介于**$O(n)$**和**$O(n^2)$**之间**，取决于 step 序列。

### 5.3.5 归并排序(Merge Sort)

递归地排序。

- 递归退出条件：列表长度为0或者1，此时有序；
- 列表长度长，就分成两部分；
- 合并：相当于合并两个有序列表。

拆分是$O(\log n)$，每次归并是$O(n)$，所以一共是$O(n \log n)$。

但是切片是$O(k)$，所以应该不用切片。

![](https://i.imgur.com/Ge31EuB.png)

*== 不用切片的话，得用一个其他的列表储存值，再还给原先的列表——但是尽管这么做，速度和用切片的没什么区别，甚至更慢 —— 我不知道为什么。 ==*

### 5.3.6 快速排序(Quick Sort)

也是递归和分治，但是不占用额外空间，直接更改。

快速排序算法首先选出一个**基准值**。尽管有很多种选法，但为简单起见，可以选取列表中的第一个元素。

**基准值的作用是帮助切分列表（一轮排序后，小于基准值的在左边，大于基准值的在右边）。**

**在最终的有序列表中**，基准值的位置通常被称作**分割点**，算法在分割点切分列表，以进行对快速排序的子调用。

![](https://i.imgur.com/kyQczo2.png)

1. 确定一个基准值，未来将小于这个值的放在左边，大于的放在右边；
2. 为了方便，假设这个基准值就是列表首位的值；
3. 双指针，分别指向`[1]`和`[end]`；
4. **大前提：右指针在左指针左边（重合也不能算）**：
   1. 首先移动左指针，直到内容大于基准值停下；
   2. 再移动右指针，直到内容小于基准值停下；
   3. 如果不满足大前提，就交换指针内容；
   4. 继续循环；
   5. 如果满足大前提（双指针刚好错位），此时左指针所在位置大于基准值，右指针所在位置小于基准值。**现在交换右指针和基准值的位置，则从左指针开始的区域都大于基准值，交换前右指针前边的区域都小于基准值。**

图解（在每次循环开始前）：

![](https://i.imgur.com/7a1SORG.jpg)

---

但这么做有一个问题：理想情况下，每次分割点都在中间，这样就是$O(n\log n)$的；但假设这是一个有序序列`[1, 2...n]`，那每次都将分成`[i, i+1...n]`和一个空列表，时间复杂度也就退化成$O(n^2)$。

一个改进的想法是**三数取中法**，从开始、中间和结尾三个数中选择一个中间的数作为基准值，因为这个数的实际位置更有希望靠近中间。

为了不破坏原有程序，将所选择的基准值和首位进行调换——这样之前的程序还可以接着用。



### 5.3.7 桶排序(Bucket Sort)

假设输入数据是整数，而且范围是已知的，比如100以内。可以根据`0~9 | 10~19 ...`把他们先分到不同的桶里；

再在每个桶里进行排序，比如用快排；

最后把每个桶的结果合并。

### 5.3.8 堆排序(Heap Sort)

用二叉堆进行排序。

先构建堆，再每次 pop 一个堆顶元素。

### 5.3.9 计数排序(Counting Sort)

假设输入的值的范围比较小，例如10以内的整数；统计每个数出现的次数，并按照次数再输出。

这个方法需要的空间较大。

### 5.3.10 基数排序(Radix Sort)

> 这个基数实际指的是进制的基数，比如十进制的基数是10。

假设都是**正整数**，而且已知最大的数有几位。

1. 把个位数是 1/2...9/0 的放在一个桶里；
2. 按顺序取出来，重组；
3. 再把十位数是1/2...9/0 的放在一个桶里；
4. 取出来，按顺序重组；
5. 循环，直到最高位。

``` python
[601, 930, 890, 735, 628, 838, 301, 146, 306, 608, 187]
[930, 890, 601, 301, 735, 146, 306, 187, 628, 838, 608]  # 按个位数
[601, 301, 306, 608, 628, 930, 735, 838, 146, 187, 890]  # 按十位数
[146, 187, 301, 306, 601, 608, 628, 735, 838, 890, 930]  # 按百位数
```



### 排序算法总结，优劣对比

![](https://i.imgur.com/5KvO9pG.png)

![](https://i.imgur.com/xB2TiyU.png)

*上图条件：只有正整数，30个，数据数量20000，数值范围1000以内*

#### 排序方法的选择

> 在随机数排序结果中，列表长度比较小时（比如20，10），快排反而比较慢，而插入和希尔排序相对较快，这是因为**插入排序和希尔排序都属于插入类型的排序**，而**快排和冒泡属于交换类排序**，数据量少时交换所消耗的资源占比大。

> 数据量较大时，快排果然还是名副其实的快：当数据集达到十万级别时，冒泡排序已经用时800多秒，而快排只用了0.3秒，相信随着数据量的增大，它们之间的差距也会越来越大。

> 在基本有序数据排序结果中，当n=10和n=100中都是插入排序消耗时间更短，因为数据基本有序，所以需要插入的次数比较少，尽管插入排序需要一个一个比较，但因为数据量不大，所以比较所消耗的资源占比不会太大。

所以数据量大时可先使用 Quick Sort，等基本有序，并且数据量比较小时再使用 Insert Sort（对少量的基本有序数据集比较好）。我个人的测试认为数据集大小为 **30左右** 的时候，Insert 和 Merge 差不多。

# 6 树

## 6.3 术语和定义

![](https://i.imgur.com/I1tWzCs.png)

![](https://i.imgur.com/tLyO7QD.png)

![](https://i.imgur.com/WHa5qWx.png)

> - 边：两个节点的连线；
> - 节点也叫key；
> - 可用Root、Child、branch表示；

## 6.4 实现方法

### 6.4.1 list of list

> 不怎么用

- 基本结构：`[root value, [left branch], [right branch]]`

- 叶子：`[value, [], []]`

- 所以每一个节点要么是长度为3，要么是`[]`；

- 这个不仅可以二叉树，其他树也可以；

![](https://i.imgur.com/AgmtuoK.png)

- insert实际上只插入了一个节点；
- 假如 insert `val`时，原来的位置有棵树`oldTree`，那`insertLeft`会把这个位置变成`[val, oldTree, []]`；
- 

### 6.4.2 节点与引用

> 遵循面向对象，常用

![](https://i.imgur.com/FCsowYJ.png)

二叉树的每个子树都是二叉树。

## 6.5 二叉树应用

### 6.5.1 解析树

> 解析树：是语法分析结果的一种表现形式,通常以树状表示语言的语法结构。

`((7 + 3) ∗ (5 − 2)) ->`  

![](https://i.imgur.com/m7DoslL.png)

从一棵空树开始：

- 左括号：为当前节点加一个左子节点，并且下沉到该节点；
- 数字：当前节点key，并返回父节点；
- 操作符：当前节点key，添加右子节点，并且下沉到该节点；
- 右括号：返回父节点；

> 只能是正整数的加减乘除

**在这里，所有的父节点满足FILO，可以用栈回退节点。**

以`(1+2)`为例，push两次，pop三次，所以一开始应该把根节点，或者空节点push进去。

操作符如何使用：

- import operator
- dict: `'+': operator.add`

### 6.5.2 树的遍历

三种遍历：

- 前序遍历：先访问根节点，然后递归地前序遍历左子树，最后递归地前序遍历右子树。（`*+73-52`）
- 后序遍历：先递归地后序遍历右子树，然后递归地后序遍历左子树，最后访问根节点。（`25-37+*`）
- 中序遍历：先递归地中序遍历左子树，然后访问根节点，最后递归地中序遍历右子树。（`7+3*5-2`），可以还原原来的表达式

**也可以改成非递归，以中序为例：**

1. 找到最小节点，并把路径上的节点都 push ；
2. pop，print
   1. 如果存在右子树，把从右子节点，到右子树的最小节点的全都push；
   2. 如果不存在右子树，pass
   3. 循环
3. 



## 6.6 二叉堆实现优先队列

> Binary Heap
>
> **每个父节点都小于等于左右节点, 但是并不意味着左右节点有大小关系**

优先队列：和队列一样FIFO，但是队列中的元素是有优先级的，按照优先级IO。I的时候就要根据特征进行优先级排列。

可以用排序O(nlogn)和插入O(n)，但是更快的方法是**二叉堆——可实现O(logn)**。分为最小堆（最小的元素在队首）和最大堆（最大的元素在队首）。

### 6.6.2 基本方法及其实现

> 可以实现一个$O(nlogn)$的排序算法

![](https://i.imgur.com/mEaHewY.png)

![](https://i.imgur.com/T2TuuTQ.png)

为了保持O(logn)这样良好的性能，应该让左右子树大小差不多，而不是一边特别大一边特别小——维持树的平衡。

> - 满二叉树：每一层都是满的；
> - 完全二叉树（此处使用）：除了最后一层，其他都是满的；并且最后一层从左往右排列；

![](https://i.imgur.com/V0R7LwS.png)

完全二叉树的神奇性质：

- 不需要list of list / node and reference，可以用一个列表表示，因为——
- 对于深度为k的一层，有$2^{k-2}$个左节点，左节点都是偶数；右节点都是奇数；
- 其中左节点分别为：$2^{k-1},\ 2^{k-1}+2\times1,\ \cdots,\ 2^{k-1}+2\times(2^{k-2}-1)=2^k-1$;
- 深度为k-1的一层，一共有$2^{k-2}$个节点，分别为$2^{k-2},\ 2^{k-2}+1,\ \cdots,\ 2^{k-2}+2^{k-2}-1=2^{k-1}-1$；
- 不难发现这两层是2倍的映射关系；
- 所以如果一个列表从1开始index（**为了实现这点，可以让第堆顶元素为一个最小值，如果要添加的元素都大于0的话**），`[p]`的左节点为`[2p]`，右节点为`[2p+1]`；
- `[p]`的父节点为`[p//2]`；
- 以上的神奇性质使得二叉堆可以用一个列表表示；

**堆的有序性**：每个父节点都小于等于左右节点，但是并不意味着k层完全大于k-1层，比如上面那张图；

具体的实现：

#### insert $O(logn)$

为了保证是个完全二叉树，应该加到队伍末尾，但是可能会破坏堆的有序性，因此需要将其进行交换。假设一个父节点只有一个子节点（子节点 > 父节点），又加入了一个节点，那么可能会有新节点 < 父节点 < 子节点，因此应该让新节点当父节点：

![](https://i.imgur.com/t03TDgo.png)

可以用递归或者循环，感觉似乎没差别，但是没有验证；

#### delMin $O(logn)$

找到最小的很简单，难点在于如何重建。

为了维持完全二叉树的形态，应该把列表最后一个移动到堆顶；然后根据parent和child的关系不断移动这个元素。

- 如果parent小于两个childs，那就没问题；
- parent应该和两个child中最小的交换；
- **循环**：直到parent小于两个childs，终止；
- **交换**：在这个过程中，交换后要先确认一个childMin，再让childMin和parent交换。然后parent为childMin，两个child根据parent可计算出；
- **问题**：
  - 但如果parent在最后一层，child就会越界，就没法比较
  - parent为末尾节点的父节点，并且该父节点只有一个子节点，也就是single child；
  - 可以用一个minChild函数，判断存在几个child，并且返回相应的值；
- 如果堆里只有1个元素（不包括为了凑数的那个），应该直接执行，不然把最后一个元素放到堆顶的操作会有问题；

#### buildHeap $O(n)$

- [ ] 一种想法是一个一个insert（O(nlogn)）；

- [ ] 一种想法是既然这是个有序数组，可以用二分法（O(logn)）找到插入的位置，但是可能会导致其他元素都移动（O(n)）—— 这样总体为（O(nlogn)）；

- [x] 书上说可以做到O(n)，但是证明太复杂不考虑；

- [x] 我想可以用py自带的排序，底层优化还是快的，直接extend；

书上的方法：

1. 直接extend；
2. 所有父节点的index是从1到`len(new_list) // 2`，只要考虑移动这些父节点就行；
3. 从最后一个父节点开始往前遍历；
4. 如果父节点大于子节点，就向下一直移动，直到满足有序性；

> 这里向下交换以满足堆的有序性的过程和delMin一样，可以把switchDown抽出来；

> 相比switch down, 常用 perc down: percolate(过滤)

## 6.7 二叉搜索树

和二叉堆不一样，二叉搜索树的目的是为了实现二分查找，因此其各节点之间的关系和之前不一样：`childLeft < parent < childRight`。

<img src="https://i.imgur.com/lsjeDcc.png" style="zoom:33%;" />

### 基本代码

> 书中直接给出

在这里的`TreeNode`更加复杂，特点包括：

- payload：即键值对中的值；
- 显式储存的parent；
- 方法：
  - 是否有LR子节点，有的话返回；
  - isChild
  - isRoot
  - isLeaf
  - 几个children
  - 更换数据**但是不更换parent**

外部的BinarySearchTree：

- 包含一个迭代器`__iter__`==？==

### put——生成或插入节点

> `put, _put, __setitem__`

put：检查有没有根节点，没有的话就`TreeNode -> root`；

有的话，就要按其他方法搜索位置。私有的辅助函数`_put(self)`：

1. 从根节点开始，比较键，然后决定左右；
2. 如果左或右节点节点为空，说明有地方可以放；没地方的话就递归；
3. `new TreeNode()`，insert；
4. 如果key一样，就更新value

### get——获取value

> `get, _get, __getitem__, __contains__`

和之前的差不多。

注意：

- `get`获取值
- `_get`获取键所在的Node
- `__getitem__`重构`[]`，可通过`[k]`访问v
- `__contains__`重构`in`

### delete——删除节点

> `delete(), __delitem__(), remove()`

#### delete主函数

基本思路：

1. `_get`找到待删除的节点；
2. 找不到key就raise error；
3. 找到了就改变size，
   1. 如果这个节点是root，置None；
   2. remove函数

#### `__delitem__`

简单地调用delete

#### remove

三种情况，取决于这个node有几个children

##### case 1: no child

删除，并且让parent没有孩子

但是要分清LR，以此判断删除parent的哪个attr

##### case2: single child

让孩子替代待删除节点。

但是要分情况：待删除节点LR，因为要改变parent的LR；

孩子改parent就行

##### case3: both children

不太可能用其中一个子节点代替，所以要想别的方法。

能不能找到一个**后继元素**代替这个节点，同时保持二叉搜索树的特征呢？

可以用**左子树的最大节点**，或者**右子树的最小节点**来代替待删除节点。

这里可以分成三个部分：

1. `findMin`：对于一个TreeNode，返回以这个节点为根节点的子树中的最小键，也就是一直往左走；
2. `findSuccessor`：对于一个待删除的节点，找到右子树的最小键，作为`succ`后继节点返回；（*这个函数里有别的condition分支，还有其他用途*）
3. `spliceOut`：删除`succ`并重建联系，这里如果递归调用`delete`会慢。**该函数适合`findMin`和`findMax`**，因为`succ`的位置是比较明确的（对于删除操作）。

![Imgur](https://i.imgur.com/Yiv89Qn.jpg)

## 6.8 平衡搜索树 AVL

### 6.8.1 概述

构建BST的时候，有可能构建出一个全是左子节点的树，相比于左右完全平衡的树，各项操作会从$O(logn)$变成$O(n)$，因为时间复杂度取决于树的深度。

AVL树是一种自动保持左右平衡的树，通过记录每个节点的平衡因子（balance factor）来保持平衡。

> 和红黑树不一样，据说红黑树更好。

平衡因子：左右子树高度之差：

- 为-1、0和1的时候都可以算平衡；
- 如果大于0就是左倾，左边更深；
- 小于0是右倾，右边更深；

![](https://i.imgur.com/k100SuI.jpg)

这个近似于斐波那契数列，而斐波那契数列两项之比趋近于$\displaystyle\frac{1+\sqrt5}{2}$...略去数学过程，可得：$h=1.44\log_2{N_h}$。

### 6.8.2 AVL实现

#### 插入 put set

在NodeTree新增属性`balanceFactor`，新class继承自`BinarySearchTree`。

平衡因子：左边高度减去右边高度。

put：overload，需要在插入的同时更新所有父节点的平衡因子。向上更新的过程中：

1. 如果一个平衡因子被变成了0，那就不会再影响上面的父节点；
2. 到了根节点，停止；
3. 如果一个节点的平衡因子不是-1、0或者1，就进行**再平衡**;

#### 再平衡 rebalance

##### 左旋实现

<img src="https://i.imgur.com/34VIKkB.png" style="zoom:50%;" />

<img src="https://i.imgur.com/WqcQ9eA.png" style="zoom:50%;" />

具体的重建connection可分为三部分：

1. `newRoot`，和`oldRoot.parent`的连接；
2. 把节点`3`和`oldRoot`连接；
3. 把`oldRoot`和`newRoot`重建连接；
4. 重新计算父节点的平衡因子：
   1. 旋转前后，非父节点的高度是不变的，因此首先把两个父节点的平衡因子用非父节点的高度表示；
   2. 写出旋转后父节点的平衡因子（用同样的非父节点的高度表示）；
   3. 对于每个节点，计算其前后变化；
   4. 能用到的数学：$\max(x,\ y)=-\min(-x,\ -y)$，$\max(x,\ y)-a=\max(x-a,\ y-a)$；

##### 右旋实现

<img src="https://i.imgur.com/coTBdlL.png" style="zoom:50%;" />

类似左旋

##### 旋转的时机

一个怎么左旋右旋都不行的例子：

![](https://i.imgur.com/RcqxP2f.png)

>  要解决这种问题，必须遵循以下规则：
> 
> - 如果子树需要左旋，首先检查右子树的平衡因子。如果右子树左倾，就对右子树做一次右旋，再围绕原节点做一次左旋；
> - 如果子树需要右旋，首先检查左子树的平衡因子。如果左子树右倾，就对左子树做一次左旋，再围绕原节点做一次右旋；
> - **如果右倾，就让右边的更加右倾；如果左倾，就让左边的更加左倾；**

![](https://i.imgur.com/9Vq9oE3.png)

#### delete

1. 如果是 leaf ，那就没事：更新向上的父节点 balance factor，必要的时候 rebalance；
2. 如果不是leaf：找 succ 替代，并重建 succ 附近的连接（`TreeNode.spliceOut`）；
3. 从 succ 的父节点开始向上更新；

# 7 图(Graph)

## 7.2 术语和定义

有一些概念和**树**类似：

- 顶点 V, **Vertex is singular of Vertices**（包括 key, payload）；
- 边 E, Edge：可以是单向、双向的；如果所有边都是单向的，称之为有向图；
- 权重：边可以带有权重——边可用三元组表示：`(start, end, weight)`；
- 子图：由一部分边和顶点构成的；
- 路径：由边连成的；
- 环：其中**有向无环图(DAG, Directed Acyclic Graph)**很有用；

![](https://i.imgur.com/VIhEsZ8.png)

## 7.3 抽象数据类型及其实现

![](https://i.imgur.com/cX3icee.png)

**两种实现方式：邻接矩阵和邻接表**

### 7.3.1 邻接矩阵

矩阵的行和列代表顶点；矩阵内的元素代表是否连接，以及权重；

但由于大部分情况下顶点之间的连接是比较**稀疏**的，因此在 python 里实现一个二维矩阵消耗资源较大；

而且在 python 里实现动态的增加、删除节点应该也不容易；

![](https://i.imgur.com/oYgPLuy.png)



### 7.3.2 邻接表

> 为了实现稀疏连接的图，更高效的方式是使用邻接表。
>
> 在邻接表实现中，我们为图对象的所有顶点保存一个主列表，同时为每一个顶点对象都维护一个列表，其中记录了与它相连的顶点。在对 Vertex 类的实现中，我们使用字典（而不是列表），字典的键是顶点，值是权重。
>
> ``` python
> class Graph -> list of vertices
> 
> class Vertex -> dict of info: {neighbor vertex: edge weight}
> ```
>
> 

![](https://i.imgur.com/yRww44b.png)

#### Vertex类实现

``` python
self.id: usually a string
self.connectedTo: a dict of nbr: weight

methods:
    addNeighbor
    __str__, __repr__
    getConnections: return self.connectedTo.keys()
	getId: self.id
    getWeight(nbr): look up dict
```

#### Graph类实现

``` python
self.verList = {id: type<'Vertex'>}
self.numVertices

methods:
    addVertex(key): add a vertex without edge
    getVertex(key): return self.verList.get(key)
	__contains__: reload in
    __iter__: reload, iter(self.vertList.values())
    addEdge(from, to, weight): ENSURE from and to in self first
    getVertices: return dict.keys()
    
```

> key 就是 id

## 7.4 BFS(Breadth First Search): Word Ladder Game

### 7.4.1 Intro

[Word Ladder](https://en.wikipedia.org/wiki/Word_ladder)：该游戏有一个起始词和一个终止词，游戏者需要发现一条连接两个词的词汇链，**词汇链上的两个相邻词只差一个字母**。游戏者一般是更改起始词中的一个字母，获得一个新词，然后继续更改所得的新词中的某个字母，再获得一个新词，最终获得终止词。 

### 7.4.2 Build Graph

![](https://i.imgur.com/gLv5qh6.png)

*A graph without weight and direction*

为了构建这个图，需要准备一个单词列表。对于每个单词，和其他单词比较是否只相差一个字母：正确的话就创建一条边。**但这个想法的时间复杂度是** $O(n^2)$。

所以：

1. 先筛选和目标单词有关的词库，比如把四个字母的单词都筛选出来；
2. 对于每个单词，比如 shit，分别匹配满足`.hit/s.it/sh.t/shi.`的单词，*把他们分别放进 4 个篮子里*；
3. 对于每个篮子里的单词，都可以通过一个字母来转换，所以没个篮子内部应该相互连接；

### 7.4.3 BFS Realize

给 vertex 类增加几个属性：

``` python
distance: 第一个 vertex 是0, 第一层是1, 以此类推
predecessor: 标记自己的上级
accessed: 该节点是否被访问过, 每一层只访问未被访问过的
```

如果发现某个节点已经被访问过，说明存在更短的路径，所以不应该再次访问：所以能知道是最短路径的长度。

`predecessor`的作用是回溯，这样就可以知道**具体的路径**。

两种实现方法，在 python 里没啥区别：

![](https://i.imgur.com/2LhJ106.jpg)

## 7.5 DFS(Depth First Search): Knight's Tour

### 7.5.1 Intro

[骑士周游问题](https://en.wikipedia.org/wiki/Knight%27s_tour)：指给定一个棋盘，骑士可以走日字，问怎么走才能不重复地遍历全部格子。

### 7.5.3 Realize(Basic Method)

用 Stack 表示待探索的队列。每次递归，将栈顶的元素作为当前元素，并将当前元素标记为“已访问”。

1. 递归退出条件：遍历路径数量等于期望值；
2. 递归缩小条件：对于每一个潜在的下一步，push 并递归；
3. 回溯条件：找到终点，或者没有下一步；
4. 如果对所有子元素，都无法找到终点，则将该节点标记为“未访问”，pop

### 7.5.4 Time Complexity Analysis(Basic Method)

最坏的情况下，需要遍历所有可能的路径才行。

假设棋盘是8864个格子，看成一棵树的话，需要找到深度63的分支；

每个父节点可能有2~8个子节点，所以时间复杂度是$O(k^n)$的：$k$是平均每个父节点有多少子节点；$n$是层数。指数阶的算法，非常耗时。

![](https://i.imgur.com/CJGOC1l.png)



### 7.5.tmp1 启发式算法技术

> 我们称利用已有知识来加速算法为启发式技术。

Warnsdorff 算法：

从上图可以发现，边缘格子的潜在子节点更少。如果我们对当前节点的子节点排个顺序，假如是子节点的潜在走法从多到少，那每次都优先遍历靠近中间的节点，因为中间的走法更多；

为了保证骑士能尽快到达边边角角，**对当前节点的子节点按照可能的走法数量从小到大排序。**

> 快了好多！



### 7.5.5 Realize(General Method)

之前的骑士周游问题，最终创建了一棵没有分支的深度优先搜索树，是一种特殊情况；通用的深度优先搜索更简单。

>一次深度优先搜索甚至能够创建多棵深度优先搜索树，我们称之为**深度优先森林**。
>
>和宽度优先搜索类似，深度优先搜索也利用**前驱连接**来构建树。

在 `Vertex` 中增加两个属性：第一次探索到该点的时间，和结束探索该点的时间。

创建一个新类：`DFSGraph(Graph)`。

``` python
class DFSGraph(Graph):
    def __init__(self):
        super().__init__()
        self.time = 0

    def dfs(self):
        for vtx in self:
            if not vtx.accessed: 
                self.dfsVisit(vtx)
        # 为了不遗漏节点，创建了多棵树；
        # 如果某个节点已经存在于某棵树内：
        # 就不会以其为根节点创建树了

    def dfsVisit(self, stVtx: Vertex):
        self.time += 1
        stVtx.accessed = True
        stVtx.disTime = self.time

        for nextVtx in stVtx.getConnections():
            if nextVtx.accessed:
                continue
            else:
                next.pred = stVtx
                self.dfsVisit(nextVtx)
        self.time += 1
        stVtx.finTime = self.time
```

关于访问时间的一个示意图：

![](https://i.imgur.com/oEmjxmj.png)

**括号特性：**DFS树中的每个子节点的时间都包含在父节点时间之内。

## 7.6 拓扑排序

> 为了展示计算机科学家可以将几乎所有问题都转换成图问题，让我们来考虑如何制作一批松饼。配方十分简单：一个鸡蛋、一杯松饼粉、一勺油，以及3/4 杯牛奶。为了制作松饼，需要加热平底锅，并将所有原材料混合后倒入锅中。当出现气泡时，将松饼翻面，继续煎至底部变成金黄色。在享用松饼之前，还会加热一些枫糖浆。 

![](https://i.imgur.com/VltHiTY.png)

> **拓扑排序**根据有向无环图生成一个包含所有顶点的线性序列，使得如果图G 中有一条边为`v->w`，那么顶点 v 排在顶点 w之前：
>
> 因此要想达到 w，就得先达到 v：***意味着应该先做 v：***
>
> 而**父节点的结束时间晚于子节点**，因此先做结束时间最晚的，最后做的结束时间最早的相当于叶子节点。



> 在很多应用中，**有向无环图被用于表明事件优先级。**
>
> 制作松饼只是其中一个例子，其他例子还包括软件项目调度、优化数据库查询的优先级表，以及矩阵相乘。

![](https://i.imgur.com/swJ3ubo.png)

*根据结束时间从大到小排列*



## 7.7 强连通单元(Strongly Connected Algorithm)

> 强连通单元图算法，可以找出图中高度连通的顶点簇：
>
> 对于图$G$，强连通单元$C$为最大的顶点子集$C\subset V$，其中对于每一对顶点$v,w\in C$，都有一条从$v$到$w$的路径和一条从$w$到$v$的路径。
>
> **然后就可以简化图**

![](https://i.imgur.com/UZ2bzUG.png)

![](https://i.imgur.com/mCI9Piw.png)

### 7.7.1 强连通算法: Kosaraju

> 不懂原理

**转置图：把有向图里的边都反过来**

![](https://i.imgur.com/KQHyeec.png)

1. 正常建一个DFSGraph，正常`dfs()`后，把各节点按照**结束访问时间递减**排序；
2. 把上一步得到的各节点 `id` ，和反向的 edge建立一个转置图；
3. 对该转置图正常 `dfs()`，就会按照期望的顺序访问节点；
4. 得到的森林就是SCCs。





### 7.7.2 Tarjan 强连通分量算法: Tarjan's Strongly Connected Components Algorithm

> Tarjan算法用于有向图，用于找强连通区域，割边等，属于图论内容。

![](https://i.imgur.com/ajL5QdJ.png)

![](https://i.imgur.com/v6EOrOZ.png)

基本方法：



1. 给每个顶点分配一个id，可以用第一次访问的时间，`dfn(depth first number)`；
2. 每个顶点还有一个`low`值，表示当前node能到达的node中最小的id（包括它自己)。
3. **具有相同 `low` 值的在同一个SCC；`low == dfn` 的是根节点**；

---

**`dfn`已经有了，问题在于怎么更新 `low`**：

三个点：

1. 不能访问重复节点：这点通过`vertex.accessed`已经实现，和普通DFS差不多；
2. `low`的初值是`dfn`；
3. 对于每个顶点，在遍历所有下家时，**实时更新`low`值**，其`low`应为本身和下家`low`的最小值；

**和下家是否在栈里没有关系！如果下家在栈里就pop，不能保证当前顶点还有未遍历的边！！**

一个实例：

![](https://i.imgur.com/4z33n0g.png)

![](https://i.imgur.com/7N1klUZ.png)

![](https://i.imgur.com/8y34qW7.png)

![](https://i.imgur.com/GiRFa5e.png)

![](https://i.imgur.com/2OyvgKV.png)

![](https://i.imgur.com/AldYHOn.png)

``` python
def dfsTarjan(self, graph):

    for vtx in graph:  # 确保不遗漏
        if not vtx.accessed:
            self._dfsTarjan(graph, vtx)
            
    # 先按照 low 排序(同一SCC在一起)，再按照 dfn 排序
    tmp = sorted(graph, key=lambda x: (x.low, x.dfn))
    # 将森林按照 dfn==low 的 root: [相同low值的元素] k-v 组成 dict
    root = None
        for _ in tmp:
            if _.low == _.dfn:
                graph.roots[_] = []
                root = _
            else:
                graph.roots[root].append(_)
            
def _dfsTarjan(self, graph, stVtx: Vertex):
    graph.time += 1
    stVtx.dfn = graph.time
    stVtx.low = stVtx.dfn
    stVtx.accessed = True

    for nextVtx in stVtx.getConnections():
        if not nextVtx.accessed:
            nextVtx.pred = stVtx
            self._dfsTarjan(graph, nextVtx)

        stVtx.low = min(stVtx.low, nextVtx.low)
```

---

事实上，上面的代码和 Stack 没啥关系......但后果是，后续还需要排序来确定，增加了时间复杂度。

**更好的做法是，利用 Stack 来实现：**

先不pop，而是在每一次递归，遍历完节点 `currVtx`的下家后：

1. 检查`cuurVtx` 的 `low==dfn`；
2. 如果`True`，说明是这是个 `root` ，而在栈里可能还有若干个SCC顶点，堆在根顶点的上面；
3. 那就 `pop`，直到把`low==dfn` 的退出来；

因为Stack里的顺序是访问的顺序。如果True，说明不可能再访问到前序节点；如果False说明还没确定根，暂时先存在栈里。

只需要在辅助函数最后加上：

``` python
if stVtx.dfn == stVtx.low:
    tmpLst = []
    while True:
        tmpVtx = self.stack.pop()
        if tmpVtx != stVtx:
            tmpLst.append(tmpVtx)
        else:
            graph.roots[stVtx] = tmpLst
            break
```



### 7.7.3 割点、割边、公共祖先(LCA, Lowest Common Ancestor)：Tarjan算法的其他妙用

> **割点(Cut Verteices, Cut Vertex)：**在一个**无向图**中，如果有一个顶点集合，删除这个顶点集合以及这个集合中所有顶点相关联的边以后，图的连通分量增多，就称这个点集为割点集合。如果去掉一个点以及与它连接的边，该点原来所在的图被分成**两部分（不连通）**，则称该点为割点。
>
> **割边(Bridge, Cut Edge)：**在一个**无向图**中，如果去掉一条边，该边原来所在的图被分成**两部分（不连通）**，则称该点为割边。





#### 割点

[CSDN上的一个帖子](https://blog.csdn.net/weixin_44179892/article/details/104196977)

基本想法差不多，都是在DFS的基础上增加时间戳和追溯值。

但SCC的low是和下家的low比较，看的是能走通的顶点：

CV的low是和dfn比较，而且只能向下不能向自己的父节点查询——这个判断是影响low更新的，**不要**和根据节点是否被访问过决定是否递归向下搜索的**逻辑混淆**了。

以下图为例，以ABCDEFGH为顺序：当D作为当前节点时，只能根据AE来更新low；但是D只能向E递归——**这是两个不同的逻辑**。

![](https://i.imgur.com/6AMO0Pq.png)

![](https://i.imgur.com/yxjKM3G.png)

上图说明：E最多只能直接访问到B，而如果要访问比B的时间戳更早的顶点A，就必须要通过B来访问。

假设存在一条通路，从E直达A，那么E的low值就是1，说明E可以不通过B直接走到A。

所以**判断割点的条件是：**

1. 对于非根节点：如果子节点的low >= 非根节点的 dfn，说明该节点是割点；
2. 对于根节点：如果在**树上**有超过1条的分支，说明去除这个根节点，就能让分支之间互不连通。

``` python
cnt = 0  # 统计每个顶点在生成树上有几个实际的子节点
for next_vtx in curr_vtx:

    if not next_vtx.accessed:
        next_vtx.pred = curr_vtx
        cnt += 1
        _cutVtxTarjan(graph, next_vtx)  # 只有下家未被访问过，才需要递归深入
        curr_vtx.low = min(curr_vtx.low, next_vtx.low)  # 下家的值会递归向上传递

    elif next_vtx != curr_vtx.pred:  # 对于最下的下家，要么没有子节点，要么就是已访问的顶点
        # 没有什么下家了，只看相连节点的dfn
        curr_vtx.low = min(curr_vtx.low, next_vtx.dfn)  

    else:  # 相连的父节点，没什么可操作的
        pass

    if curr_vtx.dfn <= next_vtx.low and curr_vtx not in graph.forest:
        graph.cut_vertices.add(curr_vtx)

if curr_vtx in graph.forest and cnt >= 2:
    graph.cut_vertices.add(curr_vtx)
```



#### 割边



​    2, 割边：对于任意有边连接的点u，v ，若**low[u] > dfn[v]**，则说明边u-v为一条割边。







## 7.8 最短路径问题: Dijkstra算法

> **考虑权重了开始**

![](https://i.imgur.com/W5WnO73.png)

一个常用的变体是，指定图中一个顶点，求所有顶点到这个指定顶点的最小距离。

适用条件：**无向，无自环**

思路：

1. 构建一个最小堆，将各个顶点按`distance`值排序；`distance`的物理意义是该节点到指定节点的距离；
2. 将指定顶点弹出来，其`distance=0`；将其作为**当前顶点**；
3. 对于**和当前节点相连，并且在堆中剩余的顶点**，更新他们的`distance`：

$$
VERTEX_{distance} = \min\left( VERTEX_{distance},\ <VERTEX,\ Current>_{distance} + Current_{distance} \right)
$$

4. 也要在堆中更新；
5. 将堆顶顶点`pop`，作为**当前顶点**；
6. `Goto 3`，直到堆空。

---

在第3步中，每个顶点的距离，要么是和起始点的直线距离，要么是经过一些不在堆里顶点中转的结果。

还可以在更新`distance`的时候顺便更新`pred`，方便追查具体的路径。

每次循环只更新和当前节点（最近一次确定最短路径的节点）之间相连的节点。

``` python
def Dijkstra(graph, st_vtx_id):
    
    # Graph[id] = Vertex inst
    # Graph.__iter__() = get vertices
    # Vertex[vertex inst] = weight
    # Vertex.__iter__() = get ceoonections

    # init
    graph[st_vtx_id].pred = graph[st_vtx_id]
    graph[st_vtx_id].distance = 0
    heap = MinBinaryHeapKV().buildHeap([[_.distance, _.id] for _ in graph])

    while not heap.isEmpty():

        curr_vtx_id = heap.delMin()[1]
        curr_vtx = graph[curr_vtx_id]

        for next_inst in (_ for _ in curr_vtx if _.id in heap):

            mid = curr_vtx.distance + curr_vtx[next_inst]
            if mid < next_inst.distance:
                next_inst.pred = curr_vtx
                next_inst.distance = mid
                heap.replace_key_by_val(next_inst.id, mid)

    pprint([f'{_.id} -> {_.distance} -> {st_vtx_id}, pred is {_.pred.id}' for _ in graph])
```





## 7.9 最小生成树(Minimum Spanning Tree, MST)：Prim算法

> **最小生成树，最小权重生成树：**一个有 n 个结点的连通图的生成树是原图的极小连通子图，且包含原图中的所有 n 个结点，并且有保持图连通的最少的边。

![](https://i.imgur.com/KRlYKyq.png)

**无控制泛滥法：**借助TTL广播，负载很大

**点对点：**为每个用户都发送一条消息，负载也比较大，比如BD会收到三条消息。

如果能构建一颗**最小生成树**的话，每个节点都只收到一条消息，并转发：A2B，B2D&C，D2E，E2F，F2G

算法思想：

可以用GA。从起始点开始，找最近的顶点；再对最近的顶点找最近的顶点——但是这样可能有遗漏。

所以正确的做法是：**确定一个顶点子集，距离顶点子集最近的点下一步被扩充到子集中。**因此每个顶点被扩充到子集中之前，都要和子集中的每个顶点比较距离。

---

初始值：

1. 所有顶点的`pred`为空，`dist`为一个很大的值，类似于无穷大。
2. 起始点的`dist`置0；
3. 构建一个堆`[vertex.dist, vertex.id]`。

**在堆不为空的情况下，循环：**

1. `pop`一个最小顶点作为`curr`；
2. 对于和`curr`相连，并且在堆中的节点`next`，检查（内循环）：
   1. 新的距离为`curr`和`next`的距离，加上`curr`的距离；
   2. 如果新的距离比`next`本身的要小，需要更新`dist=new`，`pred=curr`，`heap[dist]`。

---

每一个堆中顶点在离开堆之前，都和堆外的每个元素比较过距离。

``` python
def Prim(graph, st_vtx_id):

    # init
    graph.getVertex(st_vtx_id).distance = 0
    graph.getVertex(st_vtx_id).pred = graph.getVertex(st_vtx_id)
    heap = MinBinaryHeapKV().buildHeap([[_.distance, _.id] for _ in graph])

    while not heap.isEmpty():
        [curr_dist, curr_id] = heap.delMin()
        
        # in heap, and connected to heap
        for next_inst in (_ for _ in graph.getVertex(curr_id).getConnections() if _.id in heap):
            new_dist = graph.getVertex(curr_id).getWeight(next_inst) + curr_dist
            if new_dist < next_inst.distance:
                next_inst.distance = new_dist
                next_inst.pred = graph.getVertex(curr_id)
                heap.replace_key_by_val(next_inst.id, new_dist)

    pprint([f'{_.id} -> {_.distance} -> {st_vtx_id}, pred is {_.pred.id}' for _ in graph])
```



## 7.10 Outro

对于解决下列问题，图非常有用：

1. 利用宽度优先搜索找到无权重的最短路径。
2. 利用 Dijkstra 算法求解带权重的最短路径。
3. 利用深度优先搜索来探索图。
4. 利用 Kosaraju算法 或 Tarjan算法 求强连通单元来简化图。
5. 利用拓扑排序为任务排序。
6. 利用 Prim算法 生成最小生成树并广播消息。







