
import color
from const import WIDTH, HEIGHT, BLACK, WHITE, BLUE, RED, YELLOW
from hub import port


class ColorSensor:
    def __init__(self, port1):
        self.port1 = port1

    def get_color(self):
        c = port[self.port1]
        if c == BLACK:
            return color.BLACK
        elif c == WHITE:
            return color.WHITE
        elif c == BLUE:
            return color.BLUE
        elif c == YELLOW:
            return color.YELLOW
        elif c == RED:
            return color.RED

        return color.UNKNOWN

    def get_reflected_light(self):
        c = port[self.port1]

        if c == BLACK:
            return 50
        elif c == WHITE:
            return 100
        elif c == BLUE:
            return 75 # ??
        elif c == YELLOW:
            return 90
        elif c == RED:
            return 75 # ??

        return 50


class MotorPair:
    def __init__(self, port1, port2):
        self.port1 = port1
        self.port2 = port2

        self.default_speed = 30  # Vitesse par défaut

    def set_default_speed(self, speed):
        self.default_speed = speed
        print(f"Vitesse par défaut réglée sur {speed}%.")

    def start_tank(self, left_power, right_power):
        # time.sleep(0.5)  # Simulation du temps de réponse
        port[self.port1] = left_power
        port[self.port2] = right_power
        # print(f"Moteur gauche: {left_power}%, Moteur droit: {right_power}%.")

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