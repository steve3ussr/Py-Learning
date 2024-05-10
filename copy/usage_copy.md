# Copy

> assign_shallow_deep.py

copy分为shallow copy（浅拷贝）和deep copy（深拷贝）。这两者只在被拷贝对象内嵌套了其他对象的时候才有区别。

**Assignment**, shallow copy and **deep copy**的区别，在示例代码中（针对mutable list）如下所示：

- 赋值：
  - 两个变量名称都引用同一个对象（id相同）
  - 改变其中一个，等于改变所有
- 浅拷贝：
  - 创建新的对象（id不同）
  - 嵌套的部分使用同样的引用（修改原始list中嵌套的list中的值，也会跟着一起变：因为浅拷贝时使用了`['q', 'e']`的引用创建新列表）
- 深拷贝：
  - 创建新的对象（id不同）
  - 并且递归地创建对象，在新的内存空间完全复制一份，和原始对象完全没有关系

