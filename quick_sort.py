import random

def swap(Array, first_item_index, second_item_index):
    '''
    Given an array and two indecies, it swaps the elments in the array at the
    given indecies
    '''
    temp = Array[first_item_index]
    Array[first_item_index] = Array[second_item_index]
    Array[second_item_index] = temp

def partition(Array, left, right):
    '''
    Given an array and two boundries in the array, it partitions those
    elements such that for some (randomly chosen) element in the array,
    every element to the left of the pivot is less than the pivot, and every
    element to the right of the pivot is greater than or equal to the pivot.
    '''
    # The algorithm would work the same for any choice of pivot, and it is
    # simplest to write when you choose 'right' as your pivot, but choosing
    # a random element is recommeded since it reduces the likelihood of worst
    # case performance when the distrubtion of input arrays is not random.
    # If we were to pick 'right' as the pivot, we would have worst case
    # performance when the list was already sorted. 
    pivot_index = random.randrange(left, right + 1)
    pivot = Array[pivot_index]
    # We need to keep the pivot out of the way until the end, and our loop
    # only ranges to right - 1
    swap(Array, pivot_index, right)
    # For every element in the loop x s.t left <= x.index <= less_than_pivot, 
    # x < pivot
    less_than_pivot = left - 1
    # For every element in the loop x s.t 
    # less_than_element < x.index <= equal_to_pivot, x = pivot

    # We can ignore equal elments (i.e pick to treat them as less than or
    # greater than) but that leads to bad performance when an array has
    # lots of equal elements, because we end up doing lots of useless 
    # 'sorting' on unequal sub problems in our recursive calls.  
    equal_to_pivot = left - 1
    for i in range(left, right):
        if Array[i] == pivot:
            equal_to_pivot += 1
            swap(Array, equal_to_pivot, i)
        elif Array[i] > pivot:
            less_than_pivot += 1
            equal_to_pivot += 1
            # Every time we expand the subarray of elements less than the 
            # pivot, we need to push the elements equal to the pivot up the
            # array as well. 
            swap(Array, less_than_pivot, equal_to_pivot)
            if equal_to_pivot != i:
                swap(Array, less_than_pivot, i)
    swap(Array, equal_to_pivot + 1, right)
    return (less_than_pivot + 1, equal_to_pivot + 1)

def quick_sort(Array, left, right):
    '''
    Sorts an array, O(log(n)) in the average case and O(n^2) in the worst case.
    The worst case should be quite rare for large arrays.
    '''
    less_right_boundry, greater_left_boundry = partition(Array, left, right)
    if less_right_boundry - 1 > left:
        quick_sort(Array, left, less_right_boundry - 1)
    if greater_left_boundry + 1 < right:
        quick_sort(Array, greater_left_boundry + 1, right)


test = [4234,6,6,3,7,9,3,7,2,2,5,6,7,0,9,9,3,8,3,6]
sorted_test = sorted(test, reverse=True)
print(test)
quick_sort(test, 0, len(test) - 1)
print(test)
print(test == sorted_test)
