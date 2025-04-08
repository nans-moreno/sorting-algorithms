def insertion_sort(my_list):
    """
    Trie une liste en utilisant l'algorithme de tri par insertion.

    Args:
        my_list: La liste à trier.

    Returns:
        La liste triée.
    """
    for i in range(1, len(my_list)):
        key = my_list[i]
        j = i - 1
        while j >= 0 and my_list[j] > key:
            my_list[j + 1] = my_list[j]
            j -= 1
        my_list[j + 1] = key
    return my_list