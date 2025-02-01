import pygame
import math

from const import WIDTH, HEIGHT, WHITE, BLUE, RED, GREEN, YELLOW, BLACK, GREY
from hub import port

class Robot:
    def __init__(self, screen, x, y, angle, port1, port2, port3):
        self.screen = screen
        self.x = x
        self.y = y

        self.port1 = port1
        self.port2 = port2
        self.port3 = port3

        self.angle = angle  # Angle in degrees
        self.speed = 0  # Forward/backward speed

        self.radius = 15  # Size of the robot
        self.sensor_color = WHITE  # Default sensor color

    def draw(self):
        # Draw the robot as a circle
        pygame.draw.circle(self.screen, GREY, (int(self.x), int(self.y)), self.radius)
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
        self.angle = (self.angle + self.compute_angle(left_power, right_power)) % 360
        self.speed = self.compute_speed(left_power, right_power)
        # print(f"Angle {self.angle}. Speed {self.speed}")
        self.move()
        self.sensor_color = self.detect_color()
        port[self.port3] = self.sensor_color



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

    def detect_color(self):
        # Calculate the sensor position
        sensor_x = self.x + math.cos(math.radians(self.angle)) * (self.radius + 1)
        sensor_y = self.y - math.sin(math.radians(self.angle)) * (self.radius + 1)

        # Ensure the sensor is within bounds
        if 0 <= sensor_x < WIDTH and 0 <= sensor_y < HEIGHT:
            # Get the color of the pixel at the sensor position
            sensor_color = self.screen.get_at((int(sensor_x), int(sensor_y)))[:3]
        else:
            sensor_color = BLACK  # Default to black if out of bounds

        return sensor_color
