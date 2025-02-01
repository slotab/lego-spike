import runloop

from spike import PrimeHub, MotorPair, ColorSensor

# Initialisation du _hub, des moteurs et du capteur de couleur
hub = PrimeHub()
motors = MotorPair("A", "B")# Connectez les moteurs sur les ports A et B
color_sensor = ColorSensor("C") # Connectez le capteur de couleur sur le port C



# Configuration initiale
motors.set_default_speed(30)# Vitesse par défaut des moteurs
threshold = 50# Seuil de luminosité pour différencier la ligne et la surface (ajustez en fonction)

def follow_line():
   motors.start_tank(20, 10)
    # while True:
    #     # Lire la luminosité détectée par le capteur de couleur
    #     light_intensity = color_sensor.get_reflected_light()
    #
    #     if light_intensity < threshold:
    #         # Ligne sombre détectée : tourner légèrement à gauche
    #         motors.start_tank(20, 40)
    #     else:
    #         # Surface claire détectée : tourner légèrement à droite
    #         motors.start_tank(40, 20)


async def main():
# def main():
    try:
        motors.start_tank(20, 10)
    except KeyboardInterrupt:
        motors.stop()
        print("Programme arrêté.")

runloop.run(main()) #en mode async
# runloop.run(main)
