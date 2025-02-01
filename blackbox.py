

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