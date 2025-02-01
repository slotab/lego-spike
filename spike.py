import random
import time
import math

from const import WIDTH, HEIGHT, BLACK
from hub import port


class ColorSensor:
    def __init__(self, port, screen, robot):
        self.port = port
        self.screen = screen
        self.robot = robot
        self.simulated_light = 50  # Valeur par défaut

    def detect_color(self):
        # Calculate the sensor position
        sensor_x = self.robot.x + math.cos(math.radians(self.robot.angle)) * (self.robot.radius + 5)
        sensor_y = self.robot.y - math.sin(math.radians(self.robot.angle)) * (self.robot.radius + 5)

        # Ensure the sensor is within bounds
        if 0 <= sensor_x < WIDTH and 0 <= sensor_y < HEIGHT:
            # Get the color of the pixel at the sensor position
            self.sensor_color = self.screen.get_at((int(sensor_x), int(sensor_y)))[:3]
        else:
            self.sensor_color = BLACK  # Default to black if out of bounds

    def get_reflected_light(self):
        """
        Simule la lecture de la luminosité réfléchie.
        Retourne une valeur entre 0 (noir) et 100 (blanc).
        """
        self.simulated_light = random.randint(30, 70)  # Simulation de variation
        print(f"Capteur de couleur (port {self.port}) - Luminosité détectée: {self.simulated_light}")

        return self.simulated_light


class MotorPair:
    def __init__(self, port1, port2):
        self.port1 = port1
        self.port2 = port2

        self.default_speed = 30  # Vitesse par défaut

    def set_default_speed(self, speed):
        self.default_speed = speed
        print(f"Vitesse par défaut réglée sur {speed}%.")

    def start_tank(self, left_power, right_power):
        print(f"Moteur gauche: {left_power}%, Moteur droit: {right_power}%.")
        #time.sleep(0.5)  # Simulation du temps de réponse
        port[self.port1] = left_power
        port[self.port2] = right_power

    def stop(self):
        port[self.port1] = 0
        port[self.port2] = 0
        print("Moteurs arrêtés.")


class PrimeHub:
    def __init__(self):
        print("Hub initialisé.")

    def light_matrix(self, pattern=None):
        """Simule l'affichage sur la matrice de LED."""
        if pattern:
            print(f"Affichage sur la matrice : {pattern}")
        else:
            print("Matrice de LED éteinte.")

    def motion_sensor(self):
        """Simule un capteur de mouvement (ex: inclinaison, accélération)."""
        return {"tilt": (0, 0), "acceleration": (0, 0, 0)}

    def button_pressed(self, button_name):
        """Simule l'appui sur un bouton du _hub."""
        print(f"Bouton '{button_name}' pressé.")
        return True  # Toujours renvoyer True pour la simulation