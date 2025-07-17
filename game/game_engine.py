from .game_map import GameMap
from .renderer import Renderer
import time
import os

class GameEngine:
    def __init__(self):
        self.map = GameMap()
        self.renderer = Renderer()
        self.health = 3
        self.money = 100
        self.enemy_pos = 0
        self.waves_passed = 0
        self.towers = {}  # {(x, y): symbol}
        self.tower_types = {
            "1": {
                "symbol": "A",
                "name": "AOE Tower",
                "cost": 50,
                "desc": "Hits all enemies in 1-tile radius. Damage: 1. Range: 1 tile around tower."
            },
            "2": {
                "symbol": "L",
                "name": "Long Range Tower",
                "cost": 75,
                "desc": "Hits one enemy anywhere on the map. Damage: 2. Range: unlimited."
            },
            "3": {
                "symbol": "S",
                "name": "Slow Tower",
                "cost": 60,
                "desc": "Hits one enemy in 2-tile radius. Damage: 0. Slows enemy for 1 turn. Range: 2 tiles."
            }
        }

    def run(self):
        path = self.map.get_path()
        while self.health > 0:
            while True:
                os.system("clear")
                print("Welcome to CLI testTower Defense Game!")
                print(f"Health: {self.health}")
                print(f"Money: ${self.money}")
                print(f"Enemy Waves Passed: {self.waves_passed}")
                print("O = path, X = empty, E = enemy, A = AOE, L = Long Range, S = Slow")
                # Always show towers as active (green) in menu and placement
                self.renderer.render(path, enemy_pos=None, towers=self.towers, active_towers=set(self.towers.keys()))
                print("\nOptions:")
                print("1. Buy towers")
                print("2. Settings")
                print("3. Start wave")
                choice = input("Select an option (1-3): ").strip()
                if choice == "1":
                    self.buy_tower(path)
                elif choice == "2":
                    os.system("clear")
                    print("Settings:")
                    print("- No settings available yet.")
                    input("Press Enter to return to wave menu...")
                elif choice == "3":
                    break
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
                    input("Press Enter to continue...")

            # Enemy scaling
            num_enemies = 1 + self.waves_passed // 2
            enemy_base_health = 2 + self.waves_passed
            print(f"Wave {self.waves_passed+1}: {num_enemies} enemies, {enemy_base_health} HP each!")
            input("Press Enter to start wave...")
            # Track all enemies in the wave
            enemies = []
            for enemy_num in range(num_enemies):
                enemies.append({
                    "pos": 0,
                    "health": enemy_base_health,
                    "alive": True,
                    "slow": 0
                })
            killed_this_wave = 0
            health_lost_this_wave = 0
            while any(e["alive"] and e["pos"] < len(path) for e in enemies):
                os.system("clear")
                print("Welcome to CLI testTower Defense Game!")
                print(f"Health: {self.health}")
                print(f"Money: ${self.money}")
                print(f"Enemy Waves Passed: {self.waves_passed}")
                for idx, e in enumerate(enemies):
                    if e["alive"] and e["pos"] < len(path):
                        print(f"Enemy {idx+1}/{num_enemies} | HP: {e['health']} | Pos: {e['pos']+1}")
                print("O = path, X = empty, E = enemy, A = AOE, L = Long Range, S = Slow")
                # Render map with all alive enemies, highlight active towers and enemies
                enemy_positions = [path[e["pos"]] for e in enemies if e["alive"] and e["pos"] < len(path)]
                active_enemies = set(enemy_positions)
                # Find active towers (those affecting any enemy this turn)
                active_towers = set()
                for coord, symbol in self.towers.items():
                    for enemy_coord in enemy_positions:
                        if symbol == "A" and abs(coord[0] - enemy_coord[0]) <= 1 and abs(coord[1] - enemy_coord[1]) <= 1:
                            active_towers.add(coord)
                        elif symbol == "L":
                            active_towers.add(coord)
                        elif symbol == "S" and abs(coord[0] - enemy_coord[0]) <= 2 and abs(coord[1] - enemy_coord[1]) <= 2:
                            active_towers.add(coord)
                # Only show the first alive enemy for now (could be improved to show all)
                show_enemy_pos = None
                if enemy_positions:
                    show_enemy_pos = path.index(enemy_positions[0])
                self.renderer.render(path, show_enemy_pos, towers=self.towers, active_towers=active_towers, active_enemies=active_enemies)

                # Apply tower effects to each enemy
                for e in enemies:
                    if not e["alive"] or e["pos"] >= len(path):
                        continue
                    enemy_coord = path[e["pos"]]
                    damage = 0
                    for coord, symbol in self.towers.items():
                        if symbol == "A":
                            if abs(coord[0] - enemy_coord[0]) <= 1 and abs(coord[1] - enemy_coord[1]) <= 1:
                                damage += 1
                        elif symbol == "L":
                            damage += 2
                            break
                        elif symbol == "S":
                            if abs(coord[0] - enemy_coord[0]) <= 2 and abs(coord[1] - enemy_coord[1]) <= 2:
                                e["slow"] = 1
                    if damage > 0:
                        self.money += damage * 10
                        e["health"] -= damage
                        if e["health"] <= 0:
                            killed_this_wave += 1
                            e["alive"] = False
                    if e["slow"] > 0:
                        e["slow"] -= 1
                time.sleep(1)
                # Move all alive enemies (unless slowed)
                for e in enemies:
                    if e["alive"] and e["pos"] < len(path) and e["slow"] == 0:
                        e["pos"] += 1
                # Check for enemies reaching the end
                for e in enemies:
                    if e["alive"] and e["pos"] >= len(path):
                        self.health -= 1
                        health_lost_this_wave += 1
                        e["alive"] = False
                        time.sleep(1)
            # Show final map state at end of wave
            os.system("clear")
            print(f"Wave {self.waves_passed+1} complete!")
            print("Final map state:")
            # Show all enemy positions, including last position for killed or finished enemies
            # Only one enemy per spot in final map state
            final_enemy_positions = set()
            for e in enemies:
                if e["pos"] < len(path):
                    final_enemy_positions.add(path[e["pos"]])
                else:
                    final_enemy_positions.add(path[-1])
            self.renderer.render(path, enemy_pos=None, towers=self.towers, active_towers=set(self.towers.keys()), active_enemies=final_enemy_positions)
            print(f"Enemies killed: {killed_this_wave}")
            print(f"Health lost: {health_lost_this_wave}")
            print(f"Current Health: {self.health}")
            print(f"Current Money: ${self.money}")
            input("Press Enter to continue...")
            self.waves_passed += 1
        os.system("clear")
        print("You lost!")
        print(f"Total Enemy Waves Passed: {self.waves_passed}")

    def buy_tower(self, path):
        while True:
            os.system("clear")
            print("Buy Towers:")
            print(f"Money: ${self.money}")
            for k, v in self.tower_types.items():
                print(f"{k}. {v['name']} (${v['cost']}) - {v['desc']}")
            print("4. Cancel")
            tower_choice = input("Select tower type (1-3) or 4 to cancel: ").strip()
            if tower_choice in self.tower_types:
                tower = self.tower_types[tower_choice]
                symbol = tower['symbol']
                name = tower['name']
                cost = tower['cost']
                if self.money < cost:
                    print("Not enough money!")
                    input("Press Enter to return...")
                    return
                # Select placement
                while True:
                    os.system("clear")
                    print(f"Placing {name} (${cost})")
                    print("Select coordinates to place (e.g., 3 5), or 'c' to cancel:")
                    self.renderer.render(path, enemy_pos=None, towers=self.towers)
                    coords = input("Enter x y: ").strip()
                    if coords.lower() == 'c':
                        return
                    try:
                        x, y = map(int, coords.split())
                    except:
                        print("Invalid input. Use format: x y")
                        input("Press Enter to continue...")
                        continue
                    coord = (x, y)
                    if coord in path or coord in self.towers:
                        print("Cannot place on path or on another tower!")
                        input("Press Enter to continue...")
                        continue
                    if not (1 <= x <= 10 and 1 <= y <= 10):
                        print("Coordinates out of bounds!")
                        input("Press Enter to continue...")
                        continue
                    # Confirm placement
                    os.system("clear")
                    print(f"Confirm placement of {name} at {coord}?")
                    # Show tower placement as blue, all other towers as green
                    self.renderer.render(path, enemy_pos=None, towers=self.towers, active_towers=set(self.towers.keys()), highlight=coord)
                    confirm = input("Place here? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.towers[coord] = symbol
                        self.money -= cost
                        print(f"{name} placed at {coord}!")
                        input("Press Enter to continue...")
                        return
                    else:
                        print("Placement cancelled.")
                        input("Press Enter to continue...")
                        continue
            elif tower_choice == "4":
                return
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

"""
Game logic for CLI TD Balloons.
Run the game using:
    python3 -m game.run_game
"""
