import pygame
import math

from const import WIDTH, HEIGHT, WHITE, BLUE, RED, GREEN, YELLOW
from hub import port

# Initialize Pygame
# pygame.init()

# Screen Dimensions
#
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("LEGO SPIKE Simulator with Color Sensor")



# Clock for controlling frame rate
# clock = pygame.time.Clock()

# Robot Class
class Robot:
    def __init__(self, screen, x, y, port1, port2, port3):
        self.screen = screen
        self.x = x
        self.y = y

        self.port1 = port1
        self.port2 = port2

        self.angle = 0  # Angle in degrees
        self.speed = 0  # Forward/backward speed

        self.radius = 20  # Size of the robot
        self.sensor_color = WHITE  # Default sensor color

    def draw(self):
        # Draw the robot as a circle
        pygame.draw.circle(self.screen, BLUE, (int(self.x), int(self.y)), self.radius)
        # Draw a line indicating the direction
        direction_x = self.x + math.cos(math.radians(self.angle)) * self.radius
        direction_y = self.y - math.sin(math.radians(self.angle)) * self.radius
        pygame.draw.line(self.screen, RED, (self.x, self.y), (direction_x, direction_y), 2)

        # Draw the sensor
        pygame.draw.circle(self.screen, self.sensor_color, (int(self.x), int(self.y)), 2)

    def move(self):
        # Update position based on angle and speed
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed

    def rotate(self, direction):
        # Rotate the robot
        if direction == "left":
            self.angle += 5
        elif direction == "right":
            self.angle -= 5

    def update(self):
        left_power = port[self.port1]
        right_power = port[self.port2]
        self.angle += self.compute_angle(left_power, right_power)
        self.speed = self.compute_speed(left_power, right_power)
        print(f"Angle {self.angle}. Speed {self.speed}")
        self.move()


    def compute_angle(self, left_power: int, right_power: int) -> float:
        # Calcul de la différence entre les roues
        power_difference = right_power - left_power

        # Normalisation de l'angle entre -90° et 90°
        max_power = 100  # Supposons que 100% est la puissance max
        angle = (power_difference / max_power) * 90  # L'angle varie de -90° (gauche) à +90° (droite)
        return angle

    def compute_speed(self, left_power: int, right_power: int) -> float:
        """
        Calcule la vitesse du robot en fonction des puissances des roues.

        :param left_power: Puissance de la roue gauche (en %).
        :param right_power: Puissance de la roue droite (en %).
        :return: Vitesse du robot (de 0 à 50).
        """
        max_speed = 50  # Vitesse maximale
        avg_power = (left_power + right_power) / 2  # Moyenne des puissances
        speed = (avg_power / 100) * max_speed  # Mise à l'échelle par rapport à max_speed
        return speed

#
# # Initialize the robot
# robot = Robot(screen, WIDTH // 2, HEIGHT // 2, port.A, port.B, port.C)
#
# # Create a background with different colors
# def draw_background(screen):
#     screen.fill(WHITE)
#     pygame.draw.rect(screen, GREEN, (100, 100, 200, 200))  # Green square
#     pygame.draw.rect(screen, YELLOW, (500, 100, 200, 200))  # Yellow square
#     pygame.draw.rect(screen, RED, (100, 400, 200, 200))  # Red square
#
# # Simulation Loop
# running = True
# while running:
#     # Draw background
#     draw_background(screen)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # Get key presses
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_UP]:
#         robot.speed = 5  # Move forward
#     elif keys[pygame.K_DOWN]:
#         robot.speed = -5  # Move backward
#     else:
#         robot.speed = 0  # Stop
#
#     if keys[pygame.K_LEFT]:
#         robot.rotate("left")
#     if keys[pygame.K_RIGHT]:
#         robot.rotate("right")
#
#     # Update robot
#     robot.move()
#     #robot.detect_color()
#     robot.draw()
#
#     # Refresh display
#     pygame.display.flip()
#
#     # Limit frame rate
#     clock.tick(30)
#
# # Quit Pygame
# pygame.quit()