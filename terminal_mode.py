#!/usr/bin/env python3
'''
Mode terminal pour CosmiSort: Analyse des performances des algorithmes de tri
'''

import sys
import time
import random
from typing import List, Dict, Any, Callable, Tuple

# Import des algorithmes
from sorting import (
    selection_sort, bubble_sort, insertion_sort, 
    merge_sort, quick_sort, heap_sort, comb_sort
)

def clear_screen():
    """Efface l'écran du terminal."""
    print("\033[H\033[J", end="")

def print_header():
    """Affiche l'en-tête de CosmiSort."""
    print("\n" + "=" * 60)
    print(f"{'COSMISORT: NÉBULEUSE DU TRI':^60}")
    print("=" * 60)

def test_performance(size: int = 1000, num_tests: int = 3, timeout: int = 30):
    """
    Teste les performances des algorithmes de tri dans le terminal.
    
    Args:
        size: Taille des tableaux à trier
        num_tests: Nombre de tests à exécuter pour chaque algorithme
        timeout: Temps maximum autorisé pour chaque test (en secondes)
    """
    print(f"\nTest de performance avec {size} éléments (moyenne sur {num_tests} tests)")
    print("-" * 60)
    print(f"{'Algorithme':<25} | {'Temps (secondes)':<15} | {'Comparaison'}")
    print("-" * 60)
    
    results = {}
    
    # Liste des algorithmes à tester avec noms français et anglais
    algorithms = [
        ("Tri par sélection (Selection)", selection_sort),
        ("Tri à bulles (Bubble)", bubble_sort),
        ("Tri par insertion (Insertion)", insertion_sort),
        ("Tri fusion (Merge)", lambda x: merge_sort(x.copy())),  # merge_sort retourne une nouvelle liste
        ("Tri rapide (Quick)", quick_sort),
        ("Tri par tas (Heap)", heap_sort),
        ("Tri à peigne (Comb)", comb_sort)
    ]
    
    # Exécuter les tests
    for name, algo in algorithms:
        print(f"Testage de {name}...", end="", flush=True)
        total_time = 0
        timed_out = False
        
        for test_num in range(num_tests):
            # Générer des données aléatoires
            data = [random.randint(1, 10000) for _ in range(size)]
            test_data = data.copy()
            
            # Mesurer le temps d'exécution avec timeout
            start = time.time()
            try:
                if "Tri fusion" in name:
                    sorted_data = algo(test_data)
                else:
                    algo(test_data)
                end = time.time()
                
                duration = end - start
                if duration > timeout:
                    print(f" Timeout au test {test_num+1} ({duration:.2f}s > {timeout}s)")
                    timed_out = True
                    break
                    
                total_time += duration
                
            except Exception as e:
                print(f" Erreur: {str(e)}")
                timed_out = True
                break
        
        if timed_out:
            results[name] = float('inf')
            print(f" Temps trop long (>{timeout}s)")
        else:
            # Stocker le temps moyen
            avg_time = total_time / num_tests
            results[name] = avg_time
            print(f" Terminé en {avg_time:.6f}s")
    
    print("\nRésultats triés:")
    print("-" * 75)
    
    # Filtrer les résultats infinis
    valid_results = {k: v for k, v in results.items() if v != float('inf')}
    
    if valid_results:
        # Trouver le temps le plus rapide pour la normalisation
        fastest_time = min(valid_results.values())
        
        # Afficher les résultats triés par temps d'exécution
        for name, duration in sorted(results.items(), key=lambda x: x[1]):
            if duration == float('inf'):
                print(f"{name:<25} | {'timeout':<15} | Trop lent")
            else:
                relative = duration / fastest_time
                comparison = "x1.0 (le plus rapide)" if relative == 1.0 else f"x{relative:.2f} plus lent"
                print(f"{name:<25} | {duration:.6f}s      | {comparison}")
    else:
        print("Tous les algorithmes ont dépassé le timeout!")

def test_cas_speciaux():
    """Teste les algorithmes sur des cas spéciaux (déjà trié, inversé, doublons, etc.)"""
    print("\nTest des algorithmes sur des cas spéciaux:")
    print("-" * 60)
    
    # Définir différents cas de test
    cases = {
        "Tableau déjà trié": list(range(100)),
        "Tableau inversé": list(range(100, 0, -1)),
        "Tableau avec beaucoup de doublons": [random.randint(1, 10) for _ in range(100)],
        "Tableau presque trié (quelques éléments déplacés)": sorted([random.randint(1, 100) for _ in range(100)])
    }
    
    # Déplacer quelques éléments dans le tableau presque trié
    almost_sorted = cases["Tableau presque trié (quelques éléments déplacés)"]
    for _ in range(5):
        i, j = random.sample(range(100), 2)
        almost_sorted[i], almost_sorted[j] = almost_sorted[j], almost_sorted[i]
    
    # Liste des algorithmes à tester
    algorithms = [
        ("Tri par sélection (Selection)", selection_sort),
        ("Tri à bulles (Bubble)", bubble_sort),
        ("Tri par insertion (Insertion)", insertion_sort),
        ("Tri fusion (Merge)", lambda x: merge_sort(x.copy())),
        ("Tri rapide (Quick)", quick_sort),
        ("Tri par tas (Heap)", heap_sort),
        ("Tri à peigne (Comb)", comb_sort)
    ]
    
    # Tester chaque cas
    for case_name, data in cases.items():
        print(f"\n-- {case_name} --")
        
        results = {}
        
        for algo_name, algo in algorithms:
            # Copier les données pour ne pas les modifier
            test_data = data.copy()
            
            # Mesurer le temps d'exécution
            start = time.time()
            if "Tri fusion" in algo_name:
                sorted_data = algo(test_data)
            else:
                algo(test_data)
            end = time.time()
            
            results[algo_name] = end - start
        
        # Afficher les résultats triés
        fastest_time = min(results.values())
        print(f"{'Algorithme':<25} | {'Temps (s)':<10} | {'Efficacité relative'}")
        print("-" * 75)
        
        for name, duration in sorted(results.items(), key=lambda x: x[1]):
            relative = duration / fastest_time
            comparison = "x1.0 (le plus rapide)" if relative == 1.0 else f"x{relative:.2f}"
            print(f"{name:<25} | {duration:.6f}  | {comparison}")

def main():
    """Fonction principale du mode terminal."""
    while True:
        clear_screen()
        print_header()
        print("\nMODE TERMINAL - ANALYSE DES ALGORITHMES DE TRI")
        print("-" * 60)
        print("1. Test de performance (taille petite: 100 éléments)")
        print("2. Test de performance (taille moyenne: 500 éléments)")
        print("3. Test de performance (taille grande: 2000 éléments)")
        print("4. Test de performance (taille personnalisée)")
        print("5. Test sur cas spéciaux (déjà trié, inversé, doublons...)")
        print("6. Retour au menu principal")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            test_performance(100, 5)
        elif choix == "2":
            test_performance(500, 3)
        elif choix == "3":
            test_performance(2000, 1)
        elif choix == "4":
            try:
                taille = int(input("Entrez la taille du tableau: "))
                nb_tests = int(input("Entrez le nombre de tests à effectuer: "))
                timeout = int(input("Entrez le timeout en secondes: "))
                test_performance(taille, nb_tests, timeout)
            except ValueError:
                print("Erreur: veuillez entrer des nombres valides.")
        elif choix == "5":
            test_cas_speciaux()
        elif choix == "6":
            return
        else:
            print("Choix invalide. Veuillez réessayer.")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nUne erreur est survenue: {str(e)}")
    finally:
        print("\nFin du programme.") 