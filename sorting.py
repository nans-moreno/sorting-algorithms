def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[largest] < arr[left]:
        largest = left
    
    if right < n and arr[largest] < arr[right]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    
    # Construction du tas (heap)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extraction des éléments un par un
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    
    return arr

def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted = False
    
    while not sorted:
        # Mise à jour de l'écart
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        
        # Comparaison et échange des éléments avec l'écart
        i = 0
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1
    
    return arr