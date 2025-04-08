def quick_sort(my_list):
    """
    Trie une liste en utilisant l'algorithme de tri rapide.

    Args:
        my_list: La liste à trier.

    Returns:
        La liste triée.
    """
    if len(my_list) <= 1:
        return my_list
    else:
        pivot = my_list[0]
        less_than_pivot = [x for x in my_list[1:] if x <= pivot]
        greater_than_pivot = [x for x in my_list[1:] if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)
