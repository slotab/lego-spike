import pygame

import asyncio

from const import WHITE, GREEN, YELLOW, RED, WIDTH, HEIGHT, BLACK, BLUE, BASE_SIZE
from hub import port
from robot import Robot

# # Initialisation de Pygame
pygame.init()

# # Crée une fenêtre pour la gestion des événements (facultatif)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 14)

robot = Robot(screen, 100, 100, "A", "B", "C")

port[robot] = robot
port[screen] = screen


# # Create a background with different colors
# def draw_background(_screen):
#     _screen.fill(WHITE)
#     pygame.draw.rect(_screen, GREEN, (100, 100, 200, 200))  # Green square
#     pygame.draw.rect(_screen, YELLOW, (500, 100, 200, 200))  # Yellow square
#     pygame.draw.rect(_screen, RED, (100, 400, 200, 200))  # Red square


# Structure du labyrinthe (1 = point bleu, 2 = entrée/sortie rouge, 3 = cible jaune)
# Définition des nœuds (étiquette, x, y, largeur, hauteur, couleur)
nodes = {
    "A": (250, 100, BASE_SIZE, BASE_SIZE, RED),
    "E": (150, 200, BASE_SIZE, BASE_SIZE, BLUE),
    "F": (250, 200, BASE_SIZE, BASE_SIZE, BLUE),
    "G": (350, 200, BASE_SIZE, BASE_SIZE, BLUE),
    "K": (350, 300, BASE_SIZE, BASE_SIZE, YELLOW),
    "L": (250, 400, BASE_SIZE, BASE_SIZE, RED),
    "X": (150, 400, BASE_SIZE, BASE_SIZE, BLUE)
}

# Définition des connexions entre les nœuds
edges = [
    ("A", "F"),
    ("F", "E"), ("F", "G"),
    ("G", "K"),
    ("E", "X"),
    ("X", "L"),
]


# Fonction pour dessiner le labyrinthe
def draw_maze():
    # Dessiner les connexions (arêtes du graphe)
    for edge in edges:
        start, end = edge
        x1, y1, _, _, _ = nodes[start]
        x2, y2, _, _, _ = nodes[end]
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 5)

    # Dessiner les nœuds (sommets du graphe)
    for label, (x, y, w, h, color) in nodes.items():
        pygame.draw.rect(screen, color, (x - w//2, y - h//2, w, h))
        # Affichage du label à côté du nœud
        text_surface = font.render(label, True, BLACK)
        screen.blit(text_surface, (x + 10, y - 10))  # Décalage pour meilleure visibilité


def run(coroutine):

    print("Running...")


    # Démarre la boucle asyncio dans une tâche
    loop = asyncio.get_event_loop()
    asyncio_task = loop.create_task(coroutine)
    # ###

    running = True
    clock = pygame.time.Clock()

    # Boucle principale Pygame
    while running:
        screen.fill(WHITE)

        # Draw background
        draw_maze()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Ferme la fenêtre
                running = False

        try:
            loop.run_until_complete(asyncio_task)
            # if callable(coroutine):  # Vérifie si c'est bien une fonction
            #     coroutine()
            # else:
            #     raise TypeError("Le paramètre callback doit être une fonction.")
        except asyncio.exceptions.InvalidStateError:
            pass  # Ignore si la tâche n'est pas terminée

        robot.update()
        robot.draw()
        pygame.display.flip()
        # Limite la fréquence de rafraîchissement
        clock.tick(60)


    pygame.quit()
