import sys

import pygame

import asyncio

from const import WHITE, GREEN, YELLOW, RED, WIDTH, HEIGHT, BLACK, BLUE, BASE_SIZE, TIME
from hub import port
from robot import Robot

# # Initialisation de Pygame
pygame.init()

# # Crée une fenêtre pour la gestion des événements (facultatif)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 14)

robot = Robot(screen, 250, 50, -90, "A", "B", "C")

port[robot] = robot
port[screen] = screen


# Structure du labyrinthe (1 = point bleu, 2 = entrée/sortie rouge, 3 = cible jaune)
# Définition des nœuds (étiquette, x, y, largeur, hauteur, couleur)
nodes = {
    "A": (250, 50, BASE_SIZE, BASE_SIZE, RED),
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

async def display():

    print("Running...")
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

        robot.update()
        robot.draw()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(TIME)

    pygame.quit()
    sys.exit() # brutal close

async def sleep_ms(delay):
    await asyncio.sleep(delay)


async def pouet(coroutine):

    print("Running...")

    # # Démarre la boucle asyncio dans une tâche
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(display())
    task2 = loop.create_task(coroutine)
    await asyncio.gather(task1, task2)
    # # ###

def run(coroutine):
    asyncio.run(pouet(coroutine))
