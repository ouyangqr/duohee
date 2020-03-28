'''
@Descripttion:
@version:
@Author: XiaoYang
@Date: 2020-04-08 11:50:08
@LastEditors: XiaoYang
@LastEditTime: 2020-04-19 13:07:49
'''


def quick_sort(alist, start, end):
    """快速排序"""
    if start >= end:
        return
    lim = alist[start]

    low, high = start, end

    while low < high:
        while low < high and alist[high] >= lim:
            high -= 1
        alist[low] = alist[high]

        while low < high and alist[low] <= lim:
            low += 1
        alist[high] = alist[low]

    alist[low] = lim

    import pdb
    pdb.set_trace()
    quick_sort(alist, start, low-1)
    quick_sort(alist, low+1, end)


alist = [2, 3, 1, 4, 5, 6, ]
quick_sort(alist, 0, len(alist)-1)
print(alist)
