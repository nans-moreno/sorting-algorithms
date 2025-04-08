import time
import random
from sorting import heap_sort, comb_sort

def parse_input_list(input_string):
    try:
        elements = input_string.strip().split(',')
        numbers = [float(element.strip()) for element in elements]
        return numbers
    except ValueError:
        print("Erreur: Veuillez entrer des nombres valides séparés par des virgules.")
        return None

def format_time(seconds):
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.6f} s"

def shuffle_list(arr):
    random.shuffle(arr)
    return arr

def display_banner():
    print("\n" + "=" * 60)
    print(" ALGORITHMES DE TRI - Inspiré par Héron d'Alexandrie ")
    print("=" * 60)
    print("""
Dans l'effervescence de la ville égyptienne au Ier siècle apr. J.-C.
se dressait la Grande Bibliothèque d'Alexandrie, tel un phare
du savoir antique. Parmi les érudits arpentant les couloirs
sacrés se trouvait Héron, un esprit brillant réputé pour ses
prouesses et son habileté en mathématiques, en mécanique
et en ingénierie.
    """)

def main():
    display_banner()
    
    algorithms = {
        1: ("Tri par tas", heap_sort),
        2: ("Tri à peigne", comb_sort)
    }
    
    while True:
        print("\nOptions disponibles:")
        print("1. Importer et mélanger une liste")
        print("2. Utiliser une liste prédéfinie")
        print("0. Quitter")
        
        try:
            option = int(input("\nChoisissez une option (0-2): "))
            
            if option == 0:
                print("\nMerci d'avoir aidé Héron à organiser sa bibliothèque!")
                break
                
            if option not in [1, 2]:
                print("Option invalide. Veuillez choisir un nombre entre 0 et 2.")
                continue
            
            if option == 1:
                input_string = input("\nEntrez une liste de nombres réels séparés par des virgules: ")
                numbers = parse_input_list(input_string)
                if numbers is None:
                    continue
                
                print(f"\nListe originale: {numbers}")
                shuffled_numbers = shuffle_list(numbers.copy())
                print(f"Liste mélangée: {shuffled_numbers}")
                
                numbers_to_sort = shuffled_numbers
            else:
                numbers_to_sort = [10, 7, 8, 9, 1, 5, 3, 20, 15, 4, 6]
                print(f"\nListe prédéfinie: {numbers_to_sort}")
            
            print("\nAlgorithmes disponibles:")
            for key, (name, _) in algorithms.items():
                print(f"{key}. {name}")
            
            choice = int(input("\nChoisissez un algorithme (1-2): "))
            
            if choice not in algorithms:
                print("Choix invalide. Veuillez choisir un nombre entre 1 et 2.")
                continue
                
            algo_name, algo_func = algorithms[choice]
            
            start_time = time.time()
            sorted_numbers = algo_func(numbers_to_sort.copy())
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            print(f"\nListe triée: {sorted_numbers}")
            print(f"Algorithme utilisé: {algo_name}")
            print(f"Temps d'exécution: {format_time(execution_time)}")
            
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier valide.")
        except Exception as e:
            print(f"Une erreur est survenue: {e}")

if __name__ == "__main__":
    main()