#!/usr/bin/env python3
'''
Lanceur pour CosmiSort avec deux modes:
1. Mode graphique: visualisation des algorithmes de tri
2. Mode terminal: tests de performance, comparaisons, analyse
'''

import sys
import time

def clear_screen():
    """Efface l'écran du terminal."""
    print("\033[H\033[J", end="")

def print_header():
    """Affiche l'en-tête de CosmiSort."""
    print("\n" + "=" * 60)
    print(f"{'COSMISORT: NÉBULEUSE DU TRI':^60}")
    print("=" * 60)

def mode_graphique():
    """Lance le mode graphique (visualisation)."""
    print("\nLancement du mode graphique...")
    try:
        import main
        main.main()
    except Exception as e:
        print(f"Erreur lors du lancement du mode graphique: {str(e)}")
        input("\nAppuyez sur Entrée pour revenir au menu principal...")

def mode_terminal():
    """Lance le mode terminal pour les tests et analyses."""
    print("\nLancement du mode terminal...")
    try:
        import terminal_mode
        terminal_mode.main()
    except Exception as e:
        print(f"Erreur lors du lancement du mode terminal: {str(e)}")
        input("\nAppuyez sur Entrée pour revenir au menu principal...")

def menu_principal():
    """Affiche le menu principal."""
    while True:
        clear_screen()
        print_header()
        print("\nMENU PRINCIPAL")
        print("-" * 60)
        print("1. Mode Graphique (Visualisation)")
        print("2. Mode Terminal (Tests et Analyses)")
        print("3. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            mode_graphique()
        elif choix == "2":
            mode_terminal()
        elif choix == "3":
            print("\nMerci d'avoir utilisé CosmiSort!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nUne erreur est survenue: {str(e)}")
    finally:
        print("\nFin du programme.") 