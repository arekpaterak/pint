# function to perform quicksort
def quickSort(array: list[int], low: int, high: int) -> list[int]:
    if low < high:
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi: int = partition(array, low, high) 
        
        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)
        
        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)

def partition(array: list[int], low: int, high: int) -> int:
    # choose the rightmost element as pivot
    pivot: int = array[high] 
    
    # pointer for greater element
    i: int = low - 1 
    
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1 
            
            # Swapping element at i with element at j
            temp: int = array[j] 
            array[j] = array[i] 
            array[i] = temp
    
    # Swap the pivot element with the greater element specified by i
    temp = array[i + 1] 
    array[i + 1] = array[high] 
    array[high] = temp 
    
    # Return the position from where partition is done
    return i + 1

data: list[int] = list(1, 7, 4, 1, 10, 9, -2)
print("Unsorted Array")
print(data)

size: int = len(data)

quickSort(data, 0, size - 1)

print("Sorted Array in Ascending Order:")
print(data)
