

def bubble_sort(li):
    for j in range(len(li)-1, 0, -1):
        # print(j)
        for i in range(j):
            print(i)
            if li[i] > li[i+1]:
                li[i], li[i+1] = li[i+1], li[i]


li = [54, 26, 93, 17, 77, 31, 44, 55, 20]
bubble_sort(li)
print(li)
