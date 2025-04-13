'''
Module containing implementations of various sorting algorithms.
'''
from typing import List, TypeVar

T = TypeVar('T')  # Allows sorting lists of various comparable types

def selection_sort(data: List[T]) -> None:
    """
    Sorts a list in-place using the Selection Sort algorithm.

    Complexity:
        Time: O(n^2) average and worst case.
        Space: O(1)
    """
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        # Swap the found minimum element with the first element
        data[i], data[min_idx] = data[min_idx], data[i]

def bubble_sort(data: List[T]) -> None:
    """
    Sorts a list in-place using the Bubble Sort algorithm.

    Complexity:
        Time: O(n^2) average and worst case. O(n) best case (already sorted).
        Space: O(1)
    """
    n = len(data)
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break

def insertion_sort(data: List[T]) -> None:
    """
    Sorts a list in-place using the Insertion Sort algorithm.

    Complexity:
        Time: O(n^2) average and worst case. O(n) best case (already sorted).
        Space: O(1)
    """
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        # Move elements of data[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

def merge_sort(data: List[T]) -> List[T]:
    """
    Sorts a list using the Merge Sort algorithm (out-of-place).

    Complexity:
        Time: O(n log n) best, average, and worst case.
        Space: O(n)
    """
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        # Recursive calls for both halves
        sorted_left = merge_sort(left_half)
        sorted_right = merge_sort(right_half)

        # Merge the sorted halves
        i = j = k = 0
        merged_data = [0] * len(data) # Temporary array for merging

        while i < len(sorted_left) and j < len(sorted_right):
            if sorted_left[i] < sorted_right[j]:
                merged_data[k] = sorted_left[i]
                i += 1
            else:
                merged_data[k] = sorted_right[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(sorted_left):
            merged_data[k] = sorted_left[i]
            i += 1
            k += 1

        while j < len(sorted_right):
            merged_data[k] = sorted_right[j]
            j += 1
            k += 1
        return merged_data
    else:
        return data # Base case: list with 0 or 1 element is already sorted

def _partition(data: List[T], low: int, high: int) -> int:
    """Helper function for Quick Sort: partitions the array."""
    pivot = data[high]  # Choosing the last element as pivot
    i = low - 1       # Index of smaller element

    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if data[j] <= pivot:
            i = i + 1
            data[i], data[j] = data[j], data[i]

    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1

def quick_sort(data: List[T], low: int = None, high: int = None) -> None:
    """
    Sorts a list in-place using the Quick Sort algorithm (Lomuto partition scheme).
    Note: Initial call should be quick_sort(data).

    Complexity:
        Time: O(n log n) average case, O(n^2) worst case (rare with good pivot choice).
        Space: O(log n) average (due to recursion stack), O(n) worst case.
    """
    if low is None:
        low = 0
    if high is None:
        high = len(data) - 1

    if low < high:
        # pi is partitioning index, data[pi] is now at right place
        pi = _partition(data, low, high)

        # Separately sort elements before partition and after partition
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)

def _heapify(data: List[T], n: int, i: int) -> None:
    """Helper function for Heap Sort: ensures max-heap property."""
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2

    # See if left child of root exists and is greater than root
    if left < n and data[left] > data[largest]:
        largest = left

    # See if right child of root exists and is greater than the largest so far
    if right < n and data[right] > data[largest]:
        largest = right

    # Change root, if needed
    if largest != i:
        data[i], data[largest] = data[largest], data[i]  # Swap
        # Heapify the root.
        _heapify(data, n, largest)

def heap_sort(data: List[T]) -> None:
    """
    Sorts a list in-place using the Heap Sort algorithm.

    Complexity:
        Time: O(n log n) best, average, and worst case.
        Space: O(1)
    """
    n = len(data)

    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        _heapify(data, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]  # Swap
        _heapify(data, i, 0)

def _get_next_gap(gap: int) -> int:
    """Helper function for Comb Sort: calculates the next gap size."""
    # Shrink gap by a factor of 1.3
    gap = (gap * 10) // 13
    if gap < 1:
        return 1
    return gap

def comb_sort(data: List[T]) -> None:
    """
    Sorts a list in-place using the Comb Sort algorithm.
    An improvement over Bubble Sort.

    Complexity:
        Time: O(n^2) worst case, but average is closer to O(n log n).
        Space: O(1)
    """
    n = len(data)
    gap = n
    swapped = True

    # Keep running while gap is more than 1 or last iteration caused a swap
    while gap != 1 or swapped:
        # Find next gap
        gap = _get_next_gap(gap)
        swapped = False

        # Compare all elements with current gap
        for i in range(0, n - gap):
            if data[i] > data[i + gap]:
                data[i], data[i + gap] = data[i + gap], data[i]
                swapped = True

# --- Visualization Generators ---

def selection_sort_visual(data: List[T]):
    """Generator version of Selection Sort yielding states for visualization."""
    n = len(data)
    data_copy = list(data) # Work on a copy
    for i in range(n):
        min_idx = i
        yield {'data': list(data_copy), 'highlight': [i], 'min_candidate': min_idx} # Highlight current position and potential minimum
        for j in range(i + 1, n):
            yield {'data': list(data_copy), 'compare': [min_idx, j], 'highlight': [i]} # Highlight comparison
            if data_copy[j] < data_copy[min_idx]:
                min_idx = j
                yield {'data': list(data_copy), 'highlight': [i], 'min_candidate': min_idx} # New minimum candidate found

        # Swap
        if min_idx != i:
             data_copy[i], data_copy[min_idx] = data_copy[min_idx], data_copy[i]
             yield {'data': list(data_copy), 'swap': [i, min_idx]} # Highlight swap
        else:
             # Indicate final placement without a swap
             yield {'data': list(data_copy), 'final': [i]}

    yield {'data': list(data_copy), 'final': list(range(n))} # Final sorted state


def bubble_sort_visual(data: List[T]):
    """Generator version of Bubble Sort yielding states for visualization."""
    n = len(data)
    data_copy = list(data) # Work on a copy
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            yield {'data': list(data_copy), 'compare': [j, j + 1], 'sorted_ μέχρι': n - i} # Highlight comparison, mark sorted region
            if data_copy[j] > data_copy[j + 1]:
                data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
                swapped = True
                yield {'data': list(data_copy), 'swap': [j, j + 1], 'sorted_ μέχρι': n - i} # Highlight swap
        # Mark the last element of the pass as sorted
        yield {'data': list(data_copy), 'final': [n - 1 - i], 'sorted_ μέχρι': n - i}
        if not swapped:
            yield {'data': list(data_copy), 'final': list(range(n)), 'sorted_ μέχρι': 0} # Mark all as sorted if finished early
            break
    yield {'data': list(data_copy), 'final': list(range(n)), 'sorted_ μέχρι': 0} # Final sorted state


def insertion_sort_visual(data: List[T]):
    """Generator version of Insertion Sort yielding states for visualization."""
    data_copy = list(data) # Work on a copy
    yield {'data': list(data_copy), 'final': [0]} # First element is trivially sorted

    for i in range(1, len(data_copy)):
        key = data_copy[i]
        j = i - 1
        yield {'data': list(data_copy), 'highlight': [i], 'compare': []} # Highlight the key element being inserted

        # Indicate comparison with element j
        while j >= 0:
             yield {'data': list(data_copy), 'highlight': [i], 'compare': [j]}
             if key < data_copy[j]:
                 # Shift element j to j+1
                 data_copy[j + 1] = data_copy[j]
                 yield {'data': list(data_copy), 'highlight': [i], 'shift': [j, j+1]}
                 j -= 1
             else:
                 break # Found correct position

        # Place key at after the element just compared or at the beginning
        data_copy[j + 1] = key
        yield {'data': list(data_copy), 'insert': [j + 1], 'final': list(range(i + 1))} # Show insertion and mark sorted part

    yield {'data': list(data_copy), 'final': list(range(len(data_copy)))} # Final sorted state


def merge_sort_visual(data: List[T]):
    """Generator version of Merge Sort yielding states for visualization."""
    # Une copie complète pour le travail
    data_copy = list(data)
    
    # Un dictionnaire pour suivre les sous-tableaux (pour la visualisation)
    # Clé: (start, end), Valeur: niveau de profondeur
    subarrays = {}
    max_depth = 0
    
    def _merge_sort_internal(arr, start, end, depth=0):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        
        if end - start <= 1:  # Cas de base: liste vide ou à un élément
            if start < end:  # Uniquement pour les listes non vides
                yield {'data': list(data_copy), 'highlight': [start], 'depth': depth, 'subarrays': dict(subarrays)}
            return
        
        # Calculer le milieu pour diviser le tableau
        mid = (start + end) // 2
        
        # Ajouter les sous-tableaux au dictionnaire pour la visualisation
        subarrays[(start, mid)] = depth + 1
        subarrays[(mid, end)] = depth + 1
        
        # Afficher l'état avant la division
        yield {'data': list(data_copy), 'split': (start, mid, end), 'depth': depth, 'subarrays': dict(subarrays)}
        
        # Trier récursivement la moitié gauche
        yield from _merge_sort_internal(arr, start, mid, depth + 1)
        
        # Trier récursivement la moitié droite
        yield from _merge_sort_internal(arr, mid, end, depth + 1)
        
        # Fusionner les deux moitiés triées
        left_half = arr[start:mid]
        right_half = arr[mid:end]
        
        # Visualiser le début de la fusion
        yield {'data': list(data_copy), 'merge_start': (start, mid, end), 'depth': depth, 'subarrays': dict(subarrays)}
        
        # Fusionner les tableaux
        i = j = 0
        k = start
        
        while i < len(left_half) and j < len(right_half):
            # Comparer les éléments et choisir le plus petit
            yield {'data': list(data_copy), 'compare': [start + i, mid + j], 'depth': depth, 'subarrays': dict(subarrays)}
            
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                data_copy[k] = left_half[i]  # Mettre à jour la copie pour la visualisation
                yield {'data': list(data_copy), 'insert': [k], 'depth': depth, 'subarrays': dict(subarrays)}
                i += 1
            else:
                arr[k] = right_half[j]
                data_copy[k] = right_half[j]  # Mettre à jour la copie pour la visualisation
                yield {'data': list(data_copy), 'insert': [k], 'depth': depth, 'subarrays': dict(subarrays)}
                j += 1
            k += 1
        
        # Ajouter les éléments restants de la moitié gauche
        while i < len(left_half):
            arr[k] = left_half[i]
            data_copy[k] = left_half[i]
            yield {'data': list(data_copy), 'insert': [k], 'depth': depth, 'subarrays': dict(subarrays)}
            i += 1
            k += 1
        
        # Ajouter les éléments restants de la moitié droite
        while j < len(right_half):
            arr[k] = right_half[j]
            data_copy[k] = right_half[j]
            yield {'data': list(data_copy), 'insert': [k], 'depth': depth, 'subarrays': dict(subarrays)}
            j += 1
            k += 1
        
        # Supprimer les sous-tableaux fusionnés du dictionnaire
        if (start, mid) in subarrays:
            del subarrays[(start, mid)]
        if (mid, end) in subarrays:
            del subarrays[(mid, end)]
        
        # Marquer toute la sous-liste comme fusionnée/triée
        yield {'data': list(data_copy), 'final': list(range(start, end)), 'depth': depth, 'subarrays': dict(subarrays)}
    
    # Lancer le tri
    yield from _merge_sort_internal(data_copy, 0, len(data_copy), 0)
    
    # État final
    yield {'data': list(data_copy), 'final': list(range(len(data_copy))), 'depth': 0, 'subarrays': {}}


def quick_sort_visual(data: List[T]):
    """Generator version of Quick Sort yielding states for visualization."""
    data_copy = list(data)
    
    def _partition(arr, low, high):
        # Choisir le pivot (dernier élément)
        pivot = arr[high]
        # Yield l'état avant de commencer le partitionnement
        yield {'data': list(data_copy), 'pivot': high, 'range': (low, high)}
        
        i = low - 1  # Index de l'élément plus petit
        
        for j in range(low, high):
            # Comparer avec le pivot
            yield {'data': list(data_copy), 'compare': [j, high], 'pivot': high, 'range': (low, high)}
            
            # Si l'élément actuel est plus petit que le pivot
            if arr[j] <= pivot:
                i += 1
                # Échanger arr[i] et arr[j]
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    data_copy[i], data_copy[j] = data_copy[j], data_copy[i]
                    yield {'data': list(data_copy), 'swap': [i, j], 'pivot': high, 'range': (low, high)}
        
        # Échanger arr[i+1] et arr[high] (placer le pivot à sa position correcte)
        if i + 1 != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            data_copy[i + 1], data_copy[high] = data_copy[high], data_copy[i + 1]
            yield {'data': list(data_copy), 'swap': [i + 1, high], 'pivot_placed': i + 1, 'range': (low, high)}
        else:
            yield {'data': list(data_copy), 'pivot_placed': i + 1, 'range': (low, high)}
        
        return i + 1
    
    def _quick_sort(arr, low, high):
        if low < high:
            # Montrer la plage actuelle
            yield {'data': list(data_copy), 'highlight': list(range(low, high + 1)), 'range': (low, high)}
            
            # Partitionner et obtenir l'index du pivot
            pi_generator = _partition(arr, low, high)
            pi = None
            
            for state in pi_generator:
                yield state
                
                # Extraire l'index de pivot du dernier état
                if 'pivot_placed' in state:
                    pi = state['pivot_placed']
            
            # Marquer l'élément pivot comme étant à sa position finale
            yield {'data': list(data_copy), 'final': [pi], 'range': (low, high)}
            
            # Trier récursivement les éléments avant et après le pivot
            yield from _quick_sort(arr, low, pi - 1)
            yield from _quick_sort(arr, pi + 1, high)
        elif low == high:
            # Un seul élément est déjà trié
            yield {'data': list(data_copy), 'final': [low], 'range': (low, high)}
    
    # Si la liste est vide ou a un seul élément, c'est déjà trié
    if len(data_copy) <= 1:
        yield {'data': list(data_copy), 'final': list(range(len(data_copy)))}
        return
    
    # Lancer le tri
    yield from _quick_sort(data_copy, 0, len(data_copy) - 1)
    
    # État final
    yield {'data': list(data_copy), 'final': list(range(len(data_copy)))}


def heap_sort_visual(data: List[T]):
    """Generator version of Heap Sort yielding states for visualization."""
    data_copy = list(data)
    n = len(data_copy)
    
    def _heapify(arr, n, i):
        largest = i  # Initialiser le plus grand comme racine
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Vérifier si le fils gauche existe et est plus grand que la racine
        if left < n:
            yield {'data': list(data_copy), 'compare': [largest, left], 'heap_level': 'build'}
            if arr[left] > arr[largest]:
                largest = left
                yield {'data': list(data_copy), 'largest': largest, 'heap_level': 'build'}
        
        # Vérifier si le fils droit existe et est plus grand que le plus grand élément actuel
        if right < n:
            yield {'data': list(data_copy), 'compare': [largest, right], 'heap_level': 'build'}
            if arr[right] > arr[largest]:
                largest = right
                yield {'data': list(data_copy), 'largest': largest, 'heap_level': 'build'}
        
        # Changer la racine si nécessaire
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            data_copy[i], data_copy[largest] = data_copy[largest], data_copy[i]
            yield {'data': list(data_copy), 'swap': [i, largest], 'heap_level': 'build'}
            
            # Heapify récursivement le sous-arbre affecté
            yield from _heapify(arr, n, largest)
    
    # Construire un max heap
    for i in range(n // 2 - 1, -1, -1):
        yield {'data': list(data_copy), 'highlight': [i], 'heap_level': 'build'}
        yield from _heapify(data_copy, n, i)
    
    # Extraction des éléments un par un
    for i in range(n - 1, 0, -1):
        # Échanger la racine (maximum) avec le dernier élément
        data_copy[i], data_copy[0] = data_copy[0], data_copy[i]
        yield {'data': list(data_copy), 'swap': [0, i], 'heap_level': 'extract'}
        
        # Marquer l'élément comme étant à sa position finale
        yield {'data': list(data_copy), 'final': [i], 'heap_level': 'extract'}
        
        # Heapify la racine pour obtenir le maximum au début
        yield from _heapify(data_copy, i, 0)
    
    # Le dernier élément est également à sa place finale
    yield {'data': list(data_copy), 'final': list(range(n))}


def comb_sort_visual(data: List[T]):
    """Generator version of Comb Sort yielding states for visualization."""
    data_copy = list(data)
    n = len(data_copy)
    
    # Initialiser le gap
    gap = n
    shrink_factor = 1.3  # Facteur de réduction standard
    sorted = False
    
    while not sorted:
        # Mettre à jour le gap
        gap = int(gap / shrink_factor)
        if gap <= 1:
            gap = 1
            sorted = True  # Dernière itération
        
        yield {'data': list(data_copy), 'gap': gap}
        
        # Comparer et échanger avec le gap actuel
        for i in range(0, n - gap):
            j = i + gap
            yield {'data': list(data_copy), 'compare': [i, j], 'gap': gap}
            
            if data_copy[i] > data_copy[j]:
                data_copy[i], data_copy[j] = data_copy[j], data_copy[i]
                sorted = False  # Si des échanges sont nécessaires, la liste n'est pas triée
                yield {'data': list(data_copy), 'swap': [i, j], 'gap': gap}
    
    # Marquer tous les éléments comme étant à leur position finale
    yield {'data': list(data_copy), 'final': list(range(n))}


# NOTE: Implementing visual generators for Merge, Quick, Heap, Comb sort
# requires careful thought about how to represent their steps visually (sub-arrays, pivots, heap structure).
# Let's start with these three simpler ones and build the visualizer first.
# We will add the others progressively.


# Example Usage (Optional - for testing)
if __name__ == "__main__":
    test_data_int = [64, 34, 25, 12, 22, 11, 90, 5]
    test_data_float = [3.14, 1.618, 2.718, 0.577, 1.414, 2.236]

    print("Original Int Data:", test_data_int)
    data_copy = test_data_int[:]
    selection_sort(data_copy)
    print("Selection Sort:", data_copy)

    data_copy = test_data_int[:]
    bubble_sort(data_copy)
    print("Bubble Sort:", data_copy)

    data_copy = test_data_int[:]
    insertion_sort(data_copy)
    print("Insertion Sort:", data_copy)

    data_copy = test_data_int[:]
    sorted_merge = merge_sort(data_copy)
    print("Merge Sort:", sorted_merge)

    data_copy = test_data_int[:]
    quick_sort(data_copy)
    print("Quick Sort:", data_copy)

    data_copy = test_data_int[:]
    heap_sort(data_copy)
    print("Heap Sort:", data_copy)

    data_copy = test_data_int[:]
    comb_sort(data_copy)
    print("Comb Sort:", data_copy)

    print("\nOriginal Float Data:", test_data_float)
    data_copy = test_data_float[:]
    quick_sort(data_copy)
    print("Quick Sort (float):", data_copy) 