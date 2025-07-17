"""
Entry point for CLI TD Balloons game.
Run this file to start the game:
    python3 -m game.run_game
"""

import os
import sys
from .game_engine import GameEngine

def splash_screen():
    os.system("clear")
    print(r"""
 _____ _____ _____ 
|_   _|_   _|_   _|
  | |   | |   | |  
  | |   | |   | |  
  |_|   |_|   |_|                                                                   
                                                                         
    CLI testTower Defense Game
    """)
    print("1. Start Game")
    print("2. Options")
    print("3. Quit")

def main_menu():
    while True:
        splash_screen()
        choice = input("Select an option (1-3): ").strip()
        if choice == "1":
            engine = GameEngine()
            engine.run()
            break
        elif choice == "2":
            os.system("clear")
            print("Options:")
            print("- No options available yet.")
            input("Press Enter to return to menu...")
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
