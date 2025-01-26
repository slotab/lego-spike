import pygame
import sys
import numpy as np
import math


# Initialiser Pygame
pygame.init()

# Charger l'image
image_path = "maps/3.png"  # Remplacez par le chemin de votre image
image = pygame.image.load(image_path)

# Convertir l'image en format OpenCV (BGR)
image_cv = np.array(pygame.surfarray.pixels3d(image))


# Définir la taille de la fenêtre
window_width = image.get_width()
window_height = image.get_height()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Affichage d'image avec Event Loop")




# Obtenir la taille de l'image pour centrer dans la fenêtre
image_rect = image.get_rect(center=(window_width // 2, window_height // 2))

# Start
start = [125,465]

# Initialisation du curseur
cursor_radius = 10  # Rayon du curseur

# Taille du triangle
cursor_base = 20
cursor_height = 10

cursor_color = (0, 255, 0)  # Couleur du curseur (rouge)


# Fonction pour obtenir la couleur du pixel sous le curseur
def get_pixel_color(cursor_pos, image_cv):
    x, y = int(cursor_pos[0]), int(cursor_pos[1])
    # Obtenir la couleur du pixel sous le curseur (BGR)
    color = image_cv[x, y]
    return color


# Fonction pour obtenir le nom de la couleur en fonction des valeurs RGB
def get_color_name(color):
    r, g, b = color
    # Définir des seuils pour classer les couleurs principales
    if r > 200 and g < 100 and b < 100:
        return "Rouge"
    elif r < 100 and g > 200 and b < 100:
        return "Vert"
    elif r < 100 and g < 100 and b > 200:
        return "Bleu"
    elif r > 200 and g > 200 and b < 100:
        return "Jaune"
    elif r < 100 and g < 100 and b < 100:
        return "Noir"
    elif r > 200 and g > 200 and b > 200:
        return "Blanc"
    else:
        return "Couleur indéfinie"

def calculate_triangle_points(pos, velocity, base, height):
    """
    Calcule les points d'un triangle isocèle en fonction de la pointe avant (pos),
    du vecteur de vitesse (direction), de la base et de la hauteur.

    :param pos: Tuple (x, y), la position de la pointe avant (sommet).
    :param velocity: Tuple (vx, vy), vecteur de vitesse.
    :param base: Largeur de la base du triangle.
    :param height: Hauteur du triangle.
    :return: Liste des trois sommets du triangle [(front), (back_left), (back_right)].
    """
    vx, vy = velocity
    norm = math.sqrt(vx**2 + vy**2) or 1  # Éviter la division par 0
    direction = (vx / norm, vy / norm)

    # Calculer la position de la base (milieu de la ligne arrière)
    base_center = (
        pos[0] - direction[0] * height,
        pos[1] - direction[1] * height,
    )

    # Calculer les sommets arrière (gauche et droite)
    perpendicular = (-direction[1], direction[0])  # Perpendiculaire à la direction
    back_left = (
        base_center[0] - perpendicular[0] * base / 2,
        base_center[1] - perpendicular[1] * base / 2,
    )
    back_right = (
        base_center[0] + perpendicular[0] * base / 2,
        base_center[1] + perpendicular[1] * base / 2,
    )

    return [pos, back_left, back_right]

def rotate_cursor_velocity(velocity, angle):
    """
    Fait tourner un vecteur de vitesse selon un angle donné.

    :param velocity: Tuple (vx, vy), vecteur de vitesse initial.
    :param angle: Angle de rotation en degrés.
    :return: Nouveau vecteur de vitesse après rotation.
    """
    # Convertir l'angle en radians
    radians = math.radians(angle)

    # Décomposer le vecteur de vitesse
    vx, vy = velocity

    # Appliquer la rotation
    new_vx = vx * math.cos(radians) - vy * math.sin(radians)
    new_vy = vx * math.sin(radians) + vy * math.cos(radians)

    return new_vx, new_vy


import math

def calculate_correction_angle_gaga(last_pos, current_pos, velocity, max_correction_angle):
    # si je me dirige vers la droite et que ma position courante est à droite de la dernière position
    if last_pos[0] < current_pos[0] and velocity[0] > 0:
        return -20
    # si je me dirige vers la gauche et que ma position courante est à gauche de la dernière position
    if last_pos[0] > current_pos[0] and velocity[0] < 0:
        return 20

    # sinon pas de correction
    return 0

# fait tourner en rond...
def calculate_correction_angle(last_pos, current_pos, velocity, max_correction_angle):
    if last_pos is None:
        return 0

    """
    Calcule l'angle de correction pour ajuster la trajectoire en tenant compte de la dernière position,
    de la position courante, du vecteur de vélocité, et d'un angle de correction maximal.

    :param last_pos: Tuple (x1, y1), la dernière position connue.
    :param current_pos: Tuple (x2, y2), la position courante.
    :param velocity: Tuple (vx, vy), le vecteur de vélocité (direction du mouvement).
    :param max_correction_angle: L'angle maximal de correction en degrés.
    :return: L'angle de correction en degrés.
    """
    # Calcul du vecteur direction de la dernière position à la position actuelle
    dx1, dy1 = current_pos[0] - last_pos[0], current_pos[1] - last_pos[1]

    # Normalisation du vecteur direction
    norm1 = math.sqrt(dx1**2 + dy1**2) or 1
    direction1 = (dx1 / norm1, dy1 / norm1)

    # Normalisation du vecteur de vélocité
    vx, vy = velocity
    norm_velocity = math.sqrt(vx**2 + vy**2) or 1
    velocity_direction = (vx / norm_velocity, vy / norm_velocity)

    # Calcul du produit scalaire entre les directions
    dot_product = direction1[0] * velocity_direction[0] + direction1[1] * velocity_direction[1]

    # Calcul de l'angle en radians entre les directions
    angle_radians = math.acos(dot_product)

    # Convertir l'angle en degrés
    angle_degrees = math.degrees(angle_radians)

    # Vérifier si l'angle dépasse l'angle maximal autorisé et limiter l'angle
    if angle_degrees > max_correction_angle:
        angle_degrees = max_correction_angle

    # Retourner l'angle final
    return angle_degrees

def last_position(data, color):
    color_positions = [entry[1] for entry in data if entry[0] == color]
    if len(color_positions) < 1:
        print(f"Moins de 1 position pour la couleur {color}.")
        return None
    return  color_positions[-1]

def calculate_direction_from_positions(data, color):
    """
    Calcule la direction basée sur les deux dernières positions trouvées pour une couleur donnée.

    :param data: Liste de dictionnaires où chaque dictionnaire contient 'couleur' et 'position' (une liste de 2 éléments).
    :param color: Couleur pour laquelle la direction doit être calculée.
    :return: Vecteur direction (dx, dy), ou None si la couleur n'est pas trouvée ou moins de 2 positions.
    """
    # Filtrer les positions de la couleur donnée
    color_positions = [entry['position'] for entry in data if entry['couleur'] == color]

    if len(color_positions) < 2:
        print(f"Moins de 2 positions pour la couleur {color}. Impossible de calculer la direction.")
        return None

    # Prendre les 2 dernières positions
    last_position = color_positions[-1]
    second_last_position = color_positions[-2]

    # Calcul de la direction (vecteur) entre les 2 dernières positions
    dx = last_position[0] - second_last_position[0]
    dy = last_position[1] - second_last_position[1]

    return (dx, dy)

cursor_pos = start  # Position initiale du curseur
# Vecteur de déplacement du curseur
velocity = [0,0]  # Vecteur de déplacement (déplacement horizontal de 5 px et vertical de 3 px)
# Vitesse du curseur
speed = 5

# Boucle d'événements
running = True
following_black = False
previous_pos = None
previous_color = None
direction = [0, -1]

pouet = 0

path = []

while running:
    for event in pygame.event.get():
        # Vérifier si l'utilisateur ferme la fenêtre
        if event.type == pygame.QUIT:
            running = False

    previous_pos = cursor_pos

    if velocity[0] != 0 and velocity[1] != 0:
        direction = velocity

    # Obtenir la couleur du pixel sous le curseur
    pixel_color = get_pixel_color(cursor_pos, image_cv)
    # Obtenir le nom de la couleur
    color_name = get_color_name(pixel_color)

    path.append((color_name, previous_pos))



    # Si noir est détecté, activer le suivi
    if color_name == "Noir":
        following_black = True
        #velocity = [0, 0]
    elif color_name == "Blanc":
        last_black = last_position(path, "Noir")
        if last_black is not None:
            angle = calculate_correction_angle_gaga(last_black, cursor_pos, velocity, 45)
            velocity = rotate_cursor_velocity(velocity, angle)
        else:
            velocity = rotate_cursor_velocity(velocity, 10)
    elif color_name == "Rouge":
        if pouet <= 10:
            print("Start")
            velocity = [0, -2]
        else:
            print("Stop")
            print(path)
            velocity = [0, 0]
    # Si bleu, rouge ou jaune est détecté, arrêter le curseur
    elif color_name in ["Bleu", "Jaune"]:
        velocity = [0, 0]  # Arrêter le curseur


    previous_pos = cursor_pos
    previous_color = color_name

    # Mettre à jour la position du curseur
    cursor_pos[0] += velocity[0]
    cursor_pos[1] += velocity[1]

    # Récupérer les touches du clavier pour déplacer le curseur
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     cursor_pos[0] -= speed  # Déplacer vers la gauche
    # if keys[pygame.K_RIGHT]:
    #     cursor_pos[0] += speed  # Déplacer vers la droite
    # if keys[pygame.K_UP]:
    #     cursor_pos[1] -= speed  # Déplacer vers le haut
    # if keys[pygame.K_DOWN]:
    #     cursor_pos[1] += speed  # Déplacer vers le bas


    # Limiter la position du curseur pour qu'il ne sorte pas de la fenêtre
    cursor_pos[0] = max(0, min(cursor_pos[0], window_width - 1))
    cursor_pos[1] = max(0, min(cursor_pos[1], window_height - 1))

    # Calculer les points du triangle
    triangle_points = calculate_triangle_points(cursor_pos, direction, cursor_base, cursor_height)

    # Remplir l'écran avec une couleur (ici, noir)
    screen.fill((0, 0, 0))
    # Afficher l'image
    screen.blit(image, image_rect)
    # Afficher le curseur (un cercle rouge)
    pygame.draw.polygon(screen, cursor_color, triangle_points)
    #pygame.draw.circle(screen, (255, 0, 0), cursor_pos, 1)

    # Afficher la couleur du pixel sous le curseur
    font = pygame.font.SysFont(None, 30)
    color_text = f"Color: {color_name} {cursor_pos}"
    text_surface = font.render(color_text, True, (0, 255, 0))  # Texte en blanc
    screen.blit(text_surface, (10, 10))  # Affiche

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Définir la vitesse de la boucle (en millisecondes)
    pygame.time.Clock().tick(60)

    pouet+=1

# Quitter Pygame
pygame.quit()
sys.exit()