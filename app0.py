import asyncio

import color
import runloop
import time

from const import TIME, BLACK, BLUE
from spike import PrimeHub, MotorPair, ColorSensor

# Initialisation du _hub, des moteurs et du capteur de couleur
hub = PrimeHub()
motors = MotorPair("A", "B")# Connectez les moteurs sur les ports A et B
color_sensor = ColorSensor("C") # Connectez le capteur de couleur sur le port C



# Configuration initiale
motors.set_default_speed(30)# Vitesse par défaut des moteurs
THRESHOLD = 50

Kp = 0.5  # Gain proportionnel (à ajuster)
Ki = 0.01  # Gain intégral (peut être 0 au début)
Kd = 0.2  # Gain dérivé (évite les oscillations)

integral = 0
previous_error = 0

# Vitesse de base du robot
BASE_SPEED = 30
TARGET_REFLECT = 50  # Valeur de réflexion attendue pour une ligne noire

previous_color = None
path = []
visited_intersections = []

wait = 0

def update():


    detected_color = color_sensor.get_color()  # Récupérer la lumière réfléchie (0-100)
    left_speed = 0
    right_speed = 0

    if detected_color == color.RED:
        motors.start_tank(5, -5)
        # time.sleep(0.5)

    if detected_color == color.BLACK:
        motors.start_tank(10, 10)

    if detected_color == color.BLUE and path[-1]["color"] != color.BLUE :
        motors.start_tank(5, -5)
        wait_for_milliseconds(500)

    if detected_color == color.BLUE and path[-1]["color"] == color.BLUE :
        motors.start_tank(5, 5)

    if detected_color != color.BLACK and path[-1]["color"] == color.BLACK:
        correction = 1.2  # Facteur d'ajustement

        orientation = -1 if path[-1]["left_speed"] - path[-1]["right_speed"] > 0 else 1

        # Ajustement des vitesses en fonction de la correction
        left_speed = 10 + (correction * orientation) # Ajuste la roue gauche
        right_speed = 10 - (correction * orientation)  # Ajuste la roue droite

        # Limiter les vitesses pour éviter les dépassements
        left_speed = max(2, min(50, int(left_speed)))
        right_speed = max(2, min(50, int(right_speed)))

        # Appliquer les vitesses aux moteurs
        motors.start_tank(left_speed, right_speed)

    path.append({"color": color, "left_speed": left_speed, "right_speed": right_speed})
    # time.sleep(0.05)  # Petite pause pour la stabilité


def wait_for_milliseconds(millis):
    global wait
    wait = millis

async def main():
    global wait

    try:
        while True:
            if wait > 0:
                wait -= 1
                return

            update()
            await asyncio.sleep(TIME)

    except KeyboardInterrupt:
        motors.stop()
        print("Programme arrêté.")


if __name__ == "__main__":
    runloop.run(main())