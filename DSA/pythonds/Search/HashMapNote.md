# 关于hash函数

python内置的hash函数可能通过`id(object)`计算, 而分配内存具有随机性, 因此: 
  - 对同一对象的hash结果在**同一生命周期内应该是一样的**; 
  - 在不同生命周期内是不一样的; 
  - **非进程安全 (字符串)**, 在不同进程内不一样
  - **进程安全(非字符串)**, 在不同进程内计算结果一样
  - **线程安全**, 在同一进程内计算结果一样



```python
import multiprocessing as mp
from multiprocessing.pool import ThreadPool


def func(key):
    return hash(key)


if __name__ == '__main__':
    target = [(1564364123513464, 1232, 'a') for i in range(10000000)]
    np = 30

    res_mp = mp.Pool(processes=np).map(func, target)
    res_t = ThreadPool(processes=np).map(func, target)

    print(f"MP: {len(set(res_mp))}")
    print(f"T: {len(set(res_t))}")
```

```
MP: 30
T: 1
```



# OrderedMap的实现

> 参考: [hashmap python实现原理](https://www.cnblogs.com/Xuuuuuu/p/13894009.html)
>
> 没有使用红黑树 (因为我不会), 而是用两个辅助列表做映射和flag

## 必要的数据结构和常用数据

- `hash_raw = hash(key)`
- `hash_masked = hash_raw & (map.size-1)`
- `maxsize`: 上限, 可动态变化
- `minsize`: 下限, 应该为固定值, 也可初始化
- `item`: 包含`hash_masked, key, value`的组合

- `indices`: 建立` hash_masked` 到 `index`的映射, `index`代表这是第几个进入`dict`的`item`
- `entries`: 建立`index`到`item`的映射
- `access`: `entries`的副表, flags, 用于判断一个`item`是否被删除了

## hash算法

- `hash_raw`和`maxsize-1`与运算, 得到`hash_masked`; 这个值一定是小于等于`maxsize-1`的, 因此可确保插入`indices`

- 遇到哈希碰撞时通过**平方探测法**寻址到下一个可以插入的位置; 在每次执行"放入"操作时, `offset`初始化为0, 插入失败时令`hash_masked`加上偏移量的平方, 如果失败就递增偏移量, 继续尝试
- 本哈希表设计较为保守, 最大利用率为50%, 因此出现哈希碰撞时应当较容易解决

## 基本功能

- put: 放入item, 或者更新
- get: 获取item, 或者raise
- delete: 删除, 或者raise
- mod_size: 只要有元素数量变化, 就调用该函数, 有可能会调整尺寸
- 

## put

1. 计算hash_masked
2. 循环: 
   1. 如果hash在indices中不存在, 则顺利进入, 退出循环
   2. 如果hash在indices中存在 (哈希碰撞), 
      1. access=true, items key == new key: update, break
      2. else: continue

   3. offset + 1

3. mod_size

## get -> index

1. 计算hash_masked
2. 循环:
   1. 如果hash_masked在indices中不存在, raise KeyError
   2. 如果hash_masked在indices中存在:
      1. access=true, items.key == key, return index
      2. ~~access=false, raise KeyError~~ (**不能这么做的原因**： 假如key1已经被删除了，key2和key1哈希值相同并且已经储存起来了，当我get key2时如果先循环到了key1就会raise——实际上应该继续寻址直到index为None)
      3. access=true, items.key != key, continue

   3. offset + 1


## del

1. 调用get, 要么raise, 要么return index
2. 根据index, 将access标记为false
3. mod_size



## mod_size

1. 检测当前size是否需要容量的变化, 更改maxsize
2. 生成新的indices
3. enum zip(access, entries), 以及一个独立的cnt
   1. access=false的跳过, delete item in access and entries
   2. access=true的, 根据hash_raw重新计算hash_masked
   3. 循环：
      1. 如果hash_masked不在indices: 直接将内容更改为cnt
      2. 如果hash_masked在indices: offset+1



## print

根据access和entries, 判断key-value是否可以被打印
