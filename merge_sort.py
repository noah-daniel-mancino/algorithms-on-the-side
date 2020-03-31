test1 = [0]
test2 = [1,2,3,4,5]
test3 = [5,4,3,2,1]
test4 = [7,8,6,3,6,9,14,0]

def merge(alist):
    if len(alist) == 1:
        return alist
    else:
        merged = []
        left, right = merge(alist[:len(alist) // 2]), merge(alist[len(alist) // 2:])
        for _ in range(len(alist)):
            if left[0] < right[0]:
                merged.append(left.pop(0))
            elif right[0] <= left[0]:
                merged.append(right.pop(0))
            if not left:
                merged += right
                break
            if not right:
                merged += left
                break
        return merged


print(merge(test1))
print(merge(test2))
print(merge(test3))
print(merge(test4))
