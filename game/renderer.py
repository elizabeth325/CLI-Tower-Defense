"""
CLI rendering for testTower Defense Game.
Run the game using:
    python3 -m game.run_game
"""

class Renderer:
    def render(self, path, enemy_pos=0, x=10, y=10, towers=None, highlight=None, active_towers=None, active_enemies=None):
        enemy_coord = None
        if enemy_pos is not None:
            enemy_coord = path[enemy_pos] if enemy_pos < len(path) else None
        if towers is None:
            towers = {}
        if active_towers is None:
            active_towers = set()
        if active_enemies is None:
            active_enemies = set()
        # Print column headers with fixed width
        cell_w = 3
        header = "   " + "".join(f"{t:>{cell_w}}" for t in range(1, x+1))
        print(header)
        for j in range(y, 0, -1):
            row = f"{j:>2} "
            for t in range(1, x+1):
                coord = (t, j)
                if highlight == coord:
                    row += f"\033[34m{'B':>{cell_w-1}}\033[0m"
                elif coord in active_enemies:
                    row += f"\033[31m{'E':>{cell_w}}\033[0m"
                elif enemy_coord is not None and enemy_coord == coord:
                    row += f"{'E':>{cell_w}}"
                elif coord in active_towers:
                    row += f"\033[32m{towers[coord]:>{cell_w}}\033[0m"
                elif coord in towers:
                    row += f"{towers[coord]:>{cell_w}}"
                elif coord in path:
                    row += f"{'O':>{cell_w}}"
                else:
                    row += f"{'X':>{cell_w}}"
            print(row)
