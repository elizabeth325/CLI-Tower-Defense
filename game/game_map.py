"""
Map and path logic for CLI testTower Defense Game.
Run the game using:
    python3 -m game.run_game
"""

class GameMap:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.path = []
        self.make_path()

    def make_path(self):
        for j in range(10, 0, -1):
            self.path.append((5, j))

    def get_path(self):
        return self.path
