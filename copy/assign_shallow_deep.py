import copy


def info(x):
    print(f"object at {id(x)}: {x}")


src = ['a', 1001, ['q', 'e']]
dst_assign = src
dst_shallow = copy.copy(src)
dst_deep = copy.deepcopy(src)

info(src), info(dst_assign), info(dst_shallow), info(dst_deep)
print('-----------------------')

src[2][0] = 'dddddd'
dst_assign[0] = 'aaaa'
info(src), info(dst_assign), info(dst_shallow), info(dst_deep)
print('-----------------------')
src[1] = 1002
info(src), info(dst_assign), info(dst_shallow), info(dst_deep)
print('-----------------------')