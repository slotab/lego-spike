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

def update():
    detected_color = color_sensor.get_color()  # Récupérer la lumière réfléchie (0-100)
    left_speed = 0
    right_speed = 0

    if detected_color == color.BLACK:
        motors.start_tank(10, 10)

    if detected_color == color.BLUE and path[-1]["color"] != color.BLUE :
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


async def follow_line():
    global integral, previous_error

    while True:
        # Lire la lumière réfléchie par le capteur
        light_value = color_sensor.get_reflected_light()

        # Vérifier si on est sur un carré bleu (intersection)
        detected_color = color_sensor.get_color()
        if detected_color == color.BLUE:
            await handle_intersection()
            continue

        # Vérifier si on est sur un carré rouge (impasse ou départ)
        if detected_color == color.RED:
            await handle_dead_end()
            continue

        # Calculer l'erreur (écart par rapport à la valeur cible)
        error = TARGET_REFLECT - light_value

        # Calcul PID
        integral += error
        derivative = error - previous_error
        correction = (Kp * error) + (Ki * integral) + (Kd * derivative)

        # Calcul des vitesses des moteurs
        left_speed = BASE_SPEED + correction
        right_speed = BASE_SPEED - correction

        # Appliquer les vitesses aux moteurs
        motors.start_tank(int(left_speed),int(right_speed))

        # Mise à jour de l'erreur précédente
        previous_error = error

        await runloop.sleep_ms(TIME)
        # time.sleep(0.05)

async def handle_intersection():
    print("🔵 Intersection détectée !")
    motors.stop()
    # time.sleep(1)
    await runloop.sleep_ms(1000)

    # Vérifier si cette intersection a déjà été visitée
    if color_sensor.get_color() in visited_intersections: # fixme ??????
        print("⚠️ Intersection déjà explorée, choix d'un autre chemin...")
    else:
        visited_intersections.append(color_sensor.get_color())

    # Scanner les directions possibles et choisir la meilleure
    new_direction = choose_direction()

    if new_direction == "left":
        await turn_left()
    elif new_direction == "right":
        await turn_right()
    elif new_direction == "forward":
        pass  # Continuer tout droit

    await follow_line()

def choose_direction():
    """
    Vérifie les directions gauche, droite et avant pour voir où aller.
    """
    print("🔍 Analyse des directions...")

    # Vérifier la gauche
    turn_left()
    if detect_line():
        print("✅ Chemin trouvé à gauche")
        return "left"
    turn_right()  # Revenir en position initiale

    # Vérifier la droite
    turn_right()
    if detect_line():
        print("✅ Chemin trouvé à droite")
        return "right"
    turn_left()  # Revenir en position initiale

    # Vérifier si on peut avancer
    if detect_line():
        print("✅ Chemin trouvé en avant")
        return "forward"

    # Si aucune direction valide → Demi-tour
    print("🔄 Aucune issue, demi-tour nécessaire")
    return "back"

def detect_line():
    """
    Vérifie si une ligne noire est détectée sous le capteur.
    """
    return color_sensor.get_reflected_light() < TARGET_REFLECT + 10  # Tolérance

async def turn_left():
    """
    Effectue une rotation de 90° à gauche.
    """
    print("⬅️ Tourne à gauche")
    motors.start_tank(-20, 20)
    #time.sleep(0.6)  # Temps à ajuster selon le robot
    await runloop.sleep_ms(1200)

async def turn_right():
    """
    Effectue une rotation de 90° à droite.
    """
    print("➡️ Tourne à droite")
    motors.start_tank(20, -20)
    #time.sleep(0.6)  # Temps à ajuster selon le robot
    await runloop.sleep_ms(1200)


async def handle_dead_end():
    print("🔴 Impasse détectée ! Demi-tour en cours...")
    motors.stop()
    await runloop.sleep_ms(1000)
    #time.sleep(1)

    # Demi-tour : on fait pivoter le robot de 180 degrés
    motors.start_tank(30,-30)
    await runloop.sleep_ms(1200)
    #time.sleep(1.2)  # Temps à ajuster selon le robot

    # Reprendre la navigation
    await follow_line()

async def main():
    try:
        await follow_line()
        # while True:
        #     update()
        #     await asyncio.sleep(TIME)

    except KeyboardInterrupt:
        motors.stop()
        print("Programme arrêté.")


if __name__ == "__main__":
    runloop.run(main())