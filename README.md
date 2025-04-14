# CosmiSort: Nébuleuse du Tri

## Description
CosmiSort est une application éducative permettant d'explorer et de comparer différents algorithmes de tri. L'application propose à la fois une interface graphique futuriste inspirée du cosmos et un mode terminal pour analyser les performances des algorithmes en termes de temps d'exécution et de consommation mémoire.

## Fonctionnalités
- **Interface graphique immersive**: Visualisez les algorithmes de tri dans un environnement cosmique avec des nébuleuses et effets futuristes
- **Animation des tris**: Observez en temps réel comment les différents algorithmes organisent les données
- **Analyse de performance**: Comparez les performances de 7 algorithmes de tri différents sur des listes de différentes tailles
- **Analyse sur cas spéciaux**: Testez le comportement des algorithmes sur des cas particuliers (liste déjà triée, ordre inversé, etc.)
- **Tri de lettres**: Visualisez le fonctionnement des algorithmes sur des chaînes de caractères

## Algorithmes implémentés
- Tri par sélection (Selection Sort)
- Tri à bulles (Bubble Sort)
- Tri par insertion (Insertion Sort)
- Tri fusion (Merge Sort)
- Tri rapide (Quick Sort)
- Tri par tas (Heap Sort)
- Tri à peigne (Comb Sort)

## Utilisation
```bash
# Pour l'interface graphique futuriste avec nébuleuses
python main.py

# Pour le mode terminal analytique
python terminal_mode.py
```

## Structure du projet
- **main.py**: Interface graphique principale avec visuels cosmiques et nébuleuses
- **terminal_mode.py**: Interface utilisateur en mode terminal
- **sorting.py**: Implémentation des différents algorithmes de tri

## Interface graphique cosmique
L'interface graphique offre une expérience immersive et futuriste:
- **Thème spatial**: Arrière-plan avec nébuleuses et étoiles pour une ambiance cosmique
- **Visualisation dynamique**: Les éléments à trier sont représentés visuellement et s'animent pendant le processus de tri
- **Effets visuels**: Transitions fluides et effets lumineux lors du tri des éléments
- **Panneau de contrôle futuriste**: Interface inspirée de la science-fiction pour contrôler les paramètres de tri

## Détails techniques
- Animation fluide des processus de tri
- Effets visuels pour représenter les comparaisons et les échanges
- Analyse des performances basée sur le temps d'exécution et la consommation mémoire
- Visualisation comparative des résultats
- Options de personnalisation (taille des listes, nombre de tests, etc.)
- Gestion du timeout pour les algorithmes lents sur de grandes listes

## Explication des algorithmes

### Tri par sélection
L'algorithme parcourt le tableau, trouve l'élément minimum, et le place au début du tableau. Il répète ce processus sur la partie non triée. Complexité en O(n²).

### Tri à bulles
L'algorithme parcourt le tableau plusieurs fois, à chaque passage il compare les éléments adjacents et les échange si nécessaire. Complexité en O(n²).

### Tri par insertion
L'algorithme construit le tableau trié un élément à la fois, en insérant chaque nouvel élément à la bonne position. Complexité en O(n²).

### Tri fusion
L'algorithme divise le tableau en deux, trie récursivement chaque moitié, puis fusionne les deux moitiés triées. Complexité en O(n log n).

### Tri rapide
L'algorithme choisit un pivot, réorganise le tableau de sorte que les éléments inférieurs au pivot sont à gauche et les supérieurs à droite, puis trie récursivement les deux sous-tableaux. Complexité moyenne en O(n log n).

### Tri par tas
L'algorithme construit d'abord un tas (structure de données hiérarchique) à partir du tableau, puis extrait successivement le maximum du tas. Complexité en O(n log n).

### Tri à peigne
Version améliorée du tri à bulles qui utilise un intervalle décroissant entre les comparaisons. Complexité en O(n² / 2^p) où p est le nombre de passages.

## Caractéristiques spécifiques

### Visualisation cosmique
La représentation visuelle des algorithmes s'inspire du cosmos:
- Les éléments sont représentés comme des étoiles ou des corps célestes
- Les mouvements d'échange rappellent des orbites planétaires
- Les phases de tri sont accompagnées d'effets nébuleux et de trainées stellaires

### Analyse de mémoire
Le programme utilise `tracemalloc` pour mesurer précisément la consommation mémoire de chaque algorithme, permettant de comparer non seulement la vitesse mais aussi l'efficacité en termes d'espace.

### Mode podium
Le mode "course unique" présente les résultats sous forme de podium, facilitant la visualisation des performances relatives des différents algorithmes.

### Test sur différents types de données
Le programme permet de tester les algorithmes sur:
- Des nombres générés aléatoirement
- Des cas spécifiques (tableaux déjà triés, inversés, avec doublons)
- Des chaînes de caractères (lettres)

Ce projet a été conçu à des fins éducatives pour comprendre et visualiser les différences entre les algorithmes de tri, tout en offrant une expérience utilisateur futuriste et immersive.
 
