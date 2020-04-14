
def selection_sort(li):
    n = len(li)
    for i in range(n-1):
        # print(i)
        min_index = i
        for j in range(i+1, n):
            print(j)
            if li[j] < li[min_index]:
                min_index = j

        if min_index != i:
            li[i], li[min_index] = li[min_index], li[i]


alist = [54, 226, 93, 17, 77, 31, 44, 55, 20]
selection_sort(alist)
print(alist)
