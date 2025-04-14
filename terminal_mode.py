#!/usr/bin/env python3
'''
Mode terminal pour CosmiSort: Analyse des performances des algorithmes de tri
'''

import sys
import time
import random
import copy
import tracemalloc
from typing import List, Dict, Any, Callable, Tuple

# Import des algorithmes
from sorting import (
    selection_sort, bubble_sort, insertion_sort, 
    merge_sort, quick_sort, heap_sort, comb_sort,
    sort_letters, sort_with_explanation
)

def clear_screen():
    """Efface l'écran du terminal."""
    print("\033[H\033[J", end="")

def print_header():
    """Affiche l'en-tête de CosmiSort."""
    print("\n" + "=" * 60)
    print("COSMISORT: NÉBULEUSE DU TRI".center(60))
    print("=" * 60)

def format_memory(bytes):
    """Formate la mémoire en une chaîne lisible."""
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 * 1024:
        return f"{bytes / 1024:.2f} KB"
    else:
        return f"{bytes / (1024 * 1024):.2f} MB"

def test_performance_complet():
    """
    Teste les performances des algorithmes de tri avec des options flexibles.
    Combine l'ancien test de performance et la course des algorithmes.
    Mesure à la fois le temps d'exécution et la consommation mémoire.
    """
    clear_screen()
    print_header()
    print("\nANALYSE DE PERFORMANCE DES ALGORITHMES DE TRI")
    print("-" * 60)
    
    # Options de taille
    print("\nTailles prédéfinies :")
    print("1. Petite (100 éléments)")
    print("2. Moyenne (500 éléments)")
    print("3. Grande (2000 éléments)")
    print("4. Personnalisée")
    
    try:
        size_choice = input("\nChoisissez une taille (1-4): ")
        
        if size_choice == "1":
            size = 100
        elif size_choice == "2":
            size = 500
        elif size_choice == "3":
            size = 2000
        elif size_choice == "4":
            size = int(input("\nEntrez le nombre d'éléments: "))
            if size <= 0:
                raise ValueError("La taille doit être positive!")
        else:
            print("Choix invalide!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        # Option pour exclure les algorithmes lents pour les grandes listes
        include_all = True
        if size > 5000:
            print("\nAttention: Pour les grandes listes, les algorithmes lents (sélection, bulles, insertion)")
            print("peuvent prendre beaucoup de temps. Voulez-vous les inclure?")
            include_all = input("Inclure les algorithmes lents? (o/n): ").lower() == 'o'
        
        # Nombre de tests
        print("\nMode d'analyse :")
        print("1. Course unique (un seul test, affichage type podium)")
        print("2. Analyse statistique (plusieurs tests, calcul de moyenne)")
        
        mode_choice = input("\nChoisissez un mode (1-2): ")
        
        if mode_choice == "1":
            num_tests = 1
            mode_podium = True
        elif mode_choice == "2":
            num_tests = int(input("\nNombre de tests à exécuter (1-10): "))
            if num_tests < 1 or num_tests > 10:
                num_tests = 3
                print("Valeur invalide, utilisation de 3 tests par défaut.")
            mode_podium = False
        else:
            print("Mode invalide, utilisation du mode analyse statistique par défaut.")
            num_tests = 3
            mode_podium = False
        
        # Configuration du timeout
        timeout = int(input("\nEntrez le timeout en secondes (recommandé: 30): "))
        if timeout <= 0:
            timeout = 30
            print("Valeur invalide, utilisation du timeout de 30 secondes par défaut.")
        
        # Liste des algorithmes
        algorithms = [
            ("Tri par sélection", selection_sort),
            ("Tri à bulles", bubble_sort),
            ("Tri par insertion", insertion_sort),
            ("Tri fusion", merge_sort),
            ("Tri rapide", quick_sort),
            ("Tri par tas", heap_sort),
            ("Tri à peigne", comb_sort)
        ]
        
        # Filtrer les algorithmes si nécessaire
        if not include_all and size > 5000:
            algorithms = [algo for algo in algorithms if algo[0] not in 
                         ["Tri par sélection", "Tri à bulles", "Tri par insertion"]]
        
        # Généreration des listes de test
        print(f"\nGénération de {num_tests} liste(s) de test de {size} éléments chacune...")
        test_lists = []
        for test_num in range(num_tests):
            data = [random.randint(1, 10000) for _ in range(size)]
            print(f"  Liste de test #{test_num+1} générée ({size} éléments)")
            test_lists.append(data)
        
        print("\nDémarrage des tests (temps + mémoire)...")
        print("-" * 60)
        
        if mode_podium:
            print(f"{'Algorithme':<20} | {'Statut':<10} | {'Temps':<12} | {'Mémoire':<12} | {'Position'}")
        else:
            print(f"{'Algorithme':<20} | {'Progression':<15} | {'Temps moyen':<12} | {'Mémoire moy.'}")
        print("-" * 75)
        
        results = []
        
        # Exécuter les tests pour chaque algorithme
        for name, algo in algorithms:
            if not mode_podium:
                print(f"{name:<20} | ", end="", flush=True)
            else:
                print(f"{name:<20} | {'En cours':<10} | {'...':<12} | {'...':<12} | ...", end="\r")
                sys.stdout.flush()
            
            total_time = 0
            total_memory = 0
            timed_out = False
            error_occurred = False
            
            for test_num, original_data in enumerate(test_lists):
                # Afficher la progression si plusieurs tests
                if not mode_podium:
                    progress = f"Test {test_num+1}/{num_tests}"
                    print(f"{name:<20} | {progress:<15} | ", end="\r", flush=True)
                
                # Copier les données pour ne pas affecter les autres tests
                test_data = copy.deepcopy(original_data)
                
                # Mesurer le temps et la mémoire
                try:
                    # Démarrer la mesure de mémoire
                    tracemalloc.start()
                    
                    # Mesurer le temps d'exécution
                    start_time = time.time()
                    
                    # Traiter différemment le tri fusion qui retourne une nouvelle liste
                    sorted_data = None
                    if name == "Tri fusion":
                        sorted_data = algo(test_data)
                    else:
                        algo(test_data)
                        sorted_data = test_data
                    
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    # Mesurer la consommation mémoire
                    current, peak = tracemalloc.get_traced_memory()
                    
                    # Vérifier le timeout
                    if duration > timeout:
                        if not mode_podium:
                            print(f"{name:<20} | {'Timeout':<15} | >{timeout}s          | N/A")
                        timed_out = True
                        break
                    
                    # Vérifier que le tri est correct
                    is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
                    if not is_sorted:
                        if not mode_podium:
                            print(f"{name:<20} | {'Erreur':<15} | Tri incorrect")
                        error_occurred = True
                        break
                    
                    # Ajouter au total (pour la moyenne)
                    total_time += duration
                    total_memory += peak
                    
                except Exception as e:
                    if not mode_podium:
                        print(f"{name:<20} | {'Erreur':<15} | {str(e)}")
                    error_occurred = True
                    if tracemalloc.is_tracing():
                        tracemalloc.stop()
                    break
                
                # Arrêter la mesure de mémoire si toujours active
                if tracemalloc.is_tracing():
                    tracemalloc.stop()
            
            # Calculer les moyennes et ajouter aux résultats
            if not timed_out and not error_occurred:
                avg_time = total_time / num_tests
                avg_memory = total_memory / num_tests
                results.append((name, avg_time, avg_memory))
                
                if not mode_podium:
                    print(f"{name:<20} | {'Terminé':<15} | {avg_time:.6f}s     | {format_memory(avg_memory)}")
            elif timed_out:
                results.append((name, float('inf'), 0))
                if not mode_podium:
                    print(f"{name:<20} | {'Timeout':<15} | >{timeout}s          | N/A")
            elif error_occurred:
                results.append((name, float('inf'), 0))
                if not mode_podium:
                    print(f"{name:<20} | {'Erreur':<15} | N/A            | N/A")
            
            if mode_podium:
                # Mettre à jour le statut
                status = "Terminé" if not timed_out and not error_occurred else "Timeout" if timed_out else "Erreur"
                time_str = f"{avg_time:.6f}s" if not timed_out and not error_occurred else f">{timeout}s" if timed_out else "N/A"
                memory_str = format_memory(avg_memory) if not timed_out and not error_occurred else "N/A"
                print(f"{name:<20} | {status:<10} | {time_str:<12} | {memory_str:<12} | ...")
        
        print("\n" + "-" * 75)  # Ligne de séparation finale
        
        # Filtrer les résultats valides (temps fini)
        valid_results = [r for r in results if r[1] != float('inf')]
        
        # Trier les résultats par temps d'exécution
        valid_results.sort(key=lambda x: x[1])
        
        if mode_podium:
            print("\n" + "=" * 85)
            print("CLASSEMENT PAR TEMPS D'EXÉCUTION".center(85))
            print("=" * 85)
            
            if not valid_results:
                print("Aucun algorithme n'a terminé dans le temps imparti!")
            else:
                print("Position      | Algorithme            | Temps d'exécution  | Comparaison")
                print("-" * 85)
                
                fastest_time = valid_results[0][1]  # Le premier est le plus rapide
                
                for position, (name, duration, _) in enumerate(valid_results, 1):
                    medal = ""
                    if position == 1:
                        medal = "🥇 "
                    elif position == 2:
                        medal = "🥈 "
                    elif position == 3:
                        medal = "🥉 "
                    
                    time_relative = duration / fastest_time
                    comparison = "le plus rapide" if position == 1 else f"x{time_relative:.2f} plus lent"
                    
                    print(f"{medal}{position:<9} | {name:<20} | {duration:.6f}s{' '*(9-len(f'{duration:.6f}'))} | {comparison}")
                
                # Afficher les algorithmes qui n'ont pas terminé
                failed = [(name, time, memory) for name, time, memory in results if time == float('inf')]
                if failed:
                    print("\nAlgorithmes non classés:")
                    for name, _, _ in failed:
                        print(f"- {name:<20} | Non terminé")
                
            # DEUXIÈME TABLEAU - Classement par mémoire
            print("\n" + "=" * 85)
            print("CLASSEMENT PAR CONSOMMATION MÉMOIRE".center(85))
            print("=" * 85)
            
            if not valid_results:
                print("Aucun algorithme n'a terminé dans le temps imparti!")
            else:
                print(f"{'Position':<10} | {'Algorithme':<20} | {'Mémoire utilisée':<15} | {'Comparaison'}")
                print("-" * 85)
                
                # Trier par consommation mémoire
                memory_ranking = sorted(valid_results, key=lambda x: x[2])
                least_memory = memory_ranking[0][2]  # Le premier utilise le moins de mémoire
                
                for position, (name, duration, memory) in enumerate(memory_ranking, 1):
                    medal = ""
                    if position == 1:
                        medal = "💾 "  # Médaille pour le moins gourmand en mémoire
                    
                    memory_relative = memory / least_memory
                    memory_comparison = "le plus économe" if position == 1 else f"x{memory_relative:.2f} plus gourmand"
                    
                    print(f"{medal}{position:<9} | {name:<20} | {format_memory(memory):<15} | {memory_comparison}")
        else:
            # Mode statistique
            print("\n" + "=" * 85)
            print("ANALYSE PAR TEMPS D'EXÉCUTION".center(85))
            print("=" * 85)
            
            if not valid_results:
                print("Aucun algorithme n'a terminé dans le temps imparti!")
            else:
                # Trouver le meilleur temps pour la normalisation
                fastest_time = min(valid_results, key=lambda x: x[1])[1]
                
                print(f"{'Algorithme':<20} | {'Temps':<15} | {'Comparaison avec le plus rapide'}")
                print("-" * 85)
                
                for name, duration, _ in sorted(valid_results, key=lambda x: x[1]):
                    time_relative = duration / fastest_time
                    time_comparison = "le plus rapide" if time_relative == 1.0 else f"x{time_relative:.2f} plus lent"
                    
                    print(f"{name:<20} | {duration:.6f}s{' '*(9-len(f'{duration:.6f}'))} | {time_comparison}")
            
            # DEUXIÈME TABLEAU - Analyse par mémoire
            print("\n" + "=" * 85)
            print("ANALYSE PAR CONSOMMATION MÉMOIRE".center(85))
            print("=" * 85)
            
            if not valid_results:
                print("Aucun algorithme n'a terminé dans le temps imparti!")
            else:
                # Trouver la meilleure mémoire pour la normalisation
                least_memory = min(valid_results, key=lambda x: x[2])[2]
                
                print(f"{'Algorithme':<20} | {'Mémoire':<15} | {'Comparaison avec le plus économe'}")
                print("-" * 85)
                
                for name, _, memory in sorted(valid_results, key=lambda x: x[2]):
                    memory_relative = memory / least_memory
                    memory_comparison = "le plus économe" if memory_relative == 1.0 else f"x{memory_relative:.2f} plus gourmand"
                    
                    print(f"{name:<20} | {format_memory(memory):<15} | {memory_comparison}")
                    
    except ValueError as e:
        print(f"\nErreur: {str(e)}")
    except Exception as e:
        print(f"\nErreur inattendue: {str(e)}")
        import traceback
        traceback.print_exc()
    
    input("\nAppuyez sur Entrée pour continuer...")

def test_cas_speciaux():
    """Teste les algorithmes sur des cas spéciaux (déjà trié, inversé, doublons, etc.)"""
    clear_screen()
    print_header()
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
        ("Tri fusion (Merge)", merge_sort),
        ("Tri rapide (Quick)", quick_sort),
        ("Tri par tas (Heap)", heap_sort),
        ("Tri à peigne (Comb)", comb_sort)
    ]
    
    # Tester chaque cas
    for case_name, original_data in cases.items():
        print(f"\n-- {case_name} --")
        
        results = {}
        
        for algo_name, algo in algorithms:
            # Copier les données pour ne pas les modifier
            test_data = copy.deepcopy(original_data)
            
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
        
        print(f"\nListe originale: {original_data[:10]}{'...' if len(original_data) > 10 else ''}")
        print(f"Liste triée: {sorted(original_data[:10])}{'...' if len(original_data) > 10 else ''}")
        
    input("\nAppuyez sur Entrée pour continuer...")

def test_lettres_tri():
    """Test des algorithmes sur les lettres de l'alphabet."""
    clear_screen()
    print_header()
    print("\nTEST DE TRI DES LETTRES DE L'ALPHABET")
    print("-" * 60)
    
    # Choix de l'algorithme
    algorithms = [
        ("1", "Tri par sélection", selection_sort),
        ("2", "Tri à bulles", bubble_sort),
        ("3", "Tri par insertion", insertion_sort),
        ("4", "Tri fusion", merge_sort),
        ("5", "Tri rapide", quick_sort),
        ("6", "Tri par tas", heap_sort),
        ("7", "Tri à peigne", comb_sort)
    ]
    
    print("Algorithmes disponibles:")
    for key, name, _ in algorithms:
        print(f"{key}. {name}")
    
    algo_choice = input("\nChoisissez un algorithme (1-7): ")
    algo_dict = {key: (name, algo) for key, name, algo in algorithms}
    
    if algo_choice not in algo_dict:
        print("Choix invalide!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Récupération de l'algorithme choisi
    algo_name, algorithm = algo_dict[algo_choice]
    
    # Choix du mode de saisie
    print("\nOptions de saisie:")
    print("1. Saisir manuellement des lettres")
    print("2. Utiliser une chaîne aléatoire")
    print("3. Utiliser l'alphabet mélangé")
    
    mode_choice = input("\nVotre choix: ")
    
    if mode_choice == "1":
        # Saisie manuelle
        letters = input("\nEntrez des lettres à trier: ")
    elif mode_choice == "2":
        # Chaîne aléatoire
        length = int(input("\nCombien de lettres aléatoires (1-100): "))
        if 1 <= length <= 100:
            # Générer des lettres aléatoires (a-z, A-Z)
            letters = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length))
            print(f"\nChaîne générée: {letters}")
        else:
            print("Longueur invalide!")
            input("\nAppuyez sur Entrée pour continuer...")
            return
    elif mode_choice == "3":
        # Alphabet mélangé
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        letters = ''.join(random.sample(alphabet, len(alphabet)))
        print(f"\nAlphabet mélangé: {letters}")
    else:
        print("Option invalide!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Tri des lettres avec explication (toujours ignorer la casse)
    print("\nTri en cours...")
    start_time = time.time()
    sorted_letters, explanation = sort_with_explanation(letters, algorithm, ignore_case=True)
    end_time = time.time()
    
    # Affichage des résultats
    print("\nRÉSULTATS:")
    print("-" * 60)
    print(f"Algorithme utilisé: {algo_name}")
    print("Mode: Tri alphabétique (ignore majuscules/minuscules)")
    print(f"Chaîne originale: {letters}")
    print(f"Chaîne triée: {sorted_letters}")
    print(f"Temps d'exécution: {(end_time - start_time):.6f} secondes")
    print("\nEXPLICATION (Codes ASCII):")
    print("-" * 60)
    print(explanation)
    
    input("\nAppuyez sur Entrée pour continuer...")

def main():
    """Fonction principale du mode terminal."""
    while True:
        clear_screen()
        print_header()
        print("\nMODE TERMINAL - ANALYSE DES ALGORITHMES DE TRI")
        print("-" * 60)
        print("1. Analyse de performance des algorithmes")
        print("2. Analyse sur cas spéciaux (déjà trié, inversé...)")
        print("3. Test de tri de lettres (alphabet)")
        print("4. Retour au menu principal")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            test_performance_complet()
        elif choix == "2":
            test_cas_speciaux()
        elif choix == "3":
            test_lettres_tri()
        elif choix == "4":
            print("\nRetour au menu principal...")
            break
        else:
            print("\nOption invalide! Veuillez réessayer.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nUne erreur est survenue: {str(e)}")
    finally:
        print("\nFin du programme.") 