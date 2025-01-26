
import heapq

def a_star(graph, start, goal, heuristic):
    """
    Algorithme A* pour trouver le chemin le plus court.

    :param graph: Un dictionnaire où chaque clé est un nœud et les valeurs sont des dictionnaires de voisins avec leurs coûts.
    :param start: Nœud de départ.
    :param goal: Nœud d'objectif.
    :param heuristic: Fonction heuristique qui estime le coût du chemin restant depuis un nœud.
    :return: Une liste représentant le chemin le plus court et son coût.
    """
    # File de priorité pour A*
    open_set = []
    heapq.heappush(open_set, (0, start))  # (coût estimé total, nœud)

    # Dictionnaire pour suivre les coûts
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    # Dictionnaire pour reconstruire le chemin
    came_from = {}

    # Tant qu'il reste des nœuds à explorer
    while open_set:
        current_f_score, current_node = heapq.heappop(open_set)

        # Si on atteint l'objectif
        if current_node == goal:
            return reconstruct_path(came_from, current_node), g_score[goal]

        # Explorer les voisins
        for neighbor, cost in graph[current_node].items():
            tentative_g_score = g_score[current_node] + cost

            # Si un meilleur chemin est trouvé
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, neighbor))

    return None, float('inf')  # Aucun chemin trouvé

def reconstruct_path(came_from, current):
    """Reconstitue le chemin depuis le dictionnaire came_from."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# Exemple d'utilisation
if __name__ == "__main__":
    # Définir le graphe
    graph = {
        'A': {'B': 1, 'C': 3},
        'B': {'D': 4},
        'C': {'D': 1},
        'D': {}
    }

    # Définir une heuristique simple
    heuristic = {
        'A': 4,
        'B': 2,
        'C': 1,
        'D': 0
    }
    heuristic_function = lambda node: heuristic[node]

    # Trouver le chemin
    path, cost = a_star(graph, 'A', 'D', heuristic_function)
    print("Chemin:", path)
    print("Coût:", cost)