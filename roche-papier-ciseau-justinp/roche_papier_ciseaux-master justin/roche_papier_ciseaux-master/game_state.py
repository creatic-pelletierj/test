from enum import Enum

class GameState(Enum):
    NOT_STARTED = 0    # Le jeu n'est pas encore démarré
    ROUND_ACTIVE = 1   # Une manche est en cours
    ROUND_DONE = 2     # La manche est terminée
    GAME_OVER = 3      # Le jeu est terminé (un joueur a atteint 3 victoires)
