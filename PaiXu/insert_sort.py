

def insert_sort(li):
    for i in range(1, len(li)):
        for j in range(i, 0, -1):
            print(j)
            if li[j] < li[j-1]:
                li[j], li[j-1] = li[j-1], li[j]


alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
insert_sort(alist)
print(alist)
