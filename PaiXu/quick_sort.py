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

        while low < high and alist[low] < lim:
            low += 1
        alist[high] = alist[low]

    alist[low] = lim

    quick_sort(alist, start, low-1)
    quick_sort(alist, low+1, end)


alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
quick_sort(alist, 0, len(alist)-1)
print(alist)
