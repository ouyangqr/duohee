'''
@Descripttion:
@version:
@Author: XiaoYang
@Date: 2020-04-07 11:21:29
@LastEditors: XiaoYang
@LastEditTime: 2020-04-18 12:25:29
'''


def bubble_sort(li):
    for j in range(len(li)-1, 0, -1):
        # print(j)
        for i in range(j):
            print(i)
            if li[i] > li[i+1]:
                li[i], li[i+1] = li[i+1], li[i]


li = [54, 26, 93, 17, 77, 31, 44, 55, 20]
# bubble_sort(li)
# print(li)


for i in range(len(li)-1, 0, -1):
    for j in range(i):
        if li[j] > li[j+1]:
            li[j], li[j+1] = li[j+1], li[j]

print(li)
