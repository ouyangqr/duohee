'''
@Descripttion:
@version:
@Author: XiaoYang
@Date: 2020-04-17 15:32:52
@LastEditors: XiaoYang
@LastEditTime: 2020-04-18 12:13:37
'''

# -*- coding: utf-8 -*-


from collections import Counter


def fib_loop_while(max):
    a, b = 0, 1
    while max > 0:

        a, b = b, a + b

        max -= 1
        yield a


for i in fib_loop_while(10):
    print(i)

a = [1, 2, 3, 4, 5, 6]
for i, j in enumerate(a):
    print(i)
    print(j)
    print("1111111111111")

a = [1, 2, 3, 44, 5, 6, 6, 7, 7, 8, 8, 8, ]
a
[1, 2, 3, 44, 5, 6, 6, 7, 7, 8, 8, 8]
Counter(a)
Counter({8: 3, 6: 2, 7: 2, 1: 1, 2: 1, 3: 1, 44: 1, 5: 1})
dict(Counter(a))
{1: 1, 2: 1, 3: 1, 44: 1, 5: 1, 6: 2, 7: 2, 8: 3}
count_dict = dict(Counter(a))
for i, k in count_dict.items():
    import pdb
    pdb.set_trace()
