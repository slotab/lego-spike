import matplotlib.pyplot as plt
import numpy as np

def is_intersection(grid, row, col):
    return grid[row][col] == 2

def draw_maze(grid, start_positions, exit_position):
    """
    Dessine un labyrinthe à partir d'une grille.

    Args:
        grid (2D list): Grille du labyrinthe (1 pour chemin, 0 pour mur).
        start_positions (list of tuple): Positions des départs (ligne, colonne).
        exit_position (tuple): Position de la sortie (ligne, colonne).
    """
    rows, cols = len(grid), len(grid[0])
    fig, ax = plt.subplots(figsize=(cols, rows))

    # Dessiner les chemins
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] >= 1:
                # Dessiner les lignes noires pour les chemins
                if row > 0 and grid[row-1][col] >= 1:  # Ligne verticale
                    ax.plot([col, col], [row-1, row], color='black', linewidth=3)
                if col > 0 and grid[row][col-1] >= 1:  # Ligne horizontale
                    ax.plot([col-1, col], [row, row], color='black', linewidth=3)

    # Dessiner les intersections en bleu
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] >= 1 and is_intersection(grid, row, col):
                ax.add_patch(plt.Rectangle((col-0.1, row-0.1), 0.2, 0.2, color='blue', zorder=10))

    # Dessiner les départs en rouge
    for start in start_positions:
        ax.add_patch(plt.Rectangle((start[1]-0.1, start[0]-0.1), 0.2, 0.2, color='red', zorder=10))

    # Dessiner la sortie en jaune
    ax.add_patch(plt.Rectangle((exit_position[1]-0.1, exit_position[0]-0.1), 0.2, 0.2, color='yellow', zorder=10))

    # Configurer les axes
    ax.set_xlim(-1, cols)
    ax.set_ylim(-1, rows)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.gca().invert_yaxis()  # Inverser l'axe des Y pour correspondre à l'indexation de la grille
    plt.show()


# Exemple de grille
grid = [
    [1, 0, 2, 1, 2],
    [2, 1, 2, 0, 1],
    [0, 0, 0, 0, 1],
    [2, 1, 2, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 2, 1, 2]
]

# Départs et sortie
start_positions = [(5, 0)]  # Coordonnées des départs (impasses)
exit_position = (0, 0)  # Coordonnées de la sortie

# Dessiner le labyrinthe
draw_maze(grid, start_positions, exit_position)