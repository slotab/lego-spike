import pygame

import asyncio

from const import WHITE, GREEN, YELLOW, RED, WIDTH, HEIGHT
from hub import port
from robot import Robot

# # Initialisation de Pygame
pygame.init()

# # Crée une fenêtre pour la gestion des événements (facultatif)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spike Simulator")
robot = Robot(screen, 100, 100, "A", "B", "C")

port[robot] = robot
port[screen] = screen


# Create a background with different colors
def draw_background(_screen):
    _screen.fill(WHITE)
    pygame.draw.rect(_screen, GREEN, (100, 100, 200, 200))  # Green square
    pygame.draw.rect(_screen, YELLOW, (500, 100, 200, 200))  # Yellow square
    pygame.draw.rect(_screen, RED, (100, 400, 200, 200))  # Red square


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

        # Draw background
        draw_background(screen)

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
