#####
# TEST Move
#####
import asyncio

from pygame import time

import runloop
from const import TIME

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


async def main():
    try:
        motors.start_tank(20,20)
        await runloop.sleep_ms(2000)

        print("⬅️ Tourne à gauche")
        motors.start_tank(-20, 20)
        await runloop.sleep_ms(500)

        motors.start_tank(20, 20)
        await runloop.sleep_ms(2000)

        print("➡️ Tourne à droite")
        motors.start_tank(20, -20)
        await runloop.sleep_ms(500)

        motors.start_tank(20, 20)
        await runloop.sleep_ms(2000)

    except KeyboardInterrupt:
        motors.stop()
        print("Danse arrêté.")


if __name__ == "__main__":
    runloop.run(main())