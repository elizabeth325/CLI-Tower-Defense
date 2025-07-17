# CLI testTower Defense Game

A command-line tower defense game written in Python. Defend your base from waves of enemies by strategically placing towers on the map. Features a simple ASCII interface, multiple tower types, enemy scaling, and color-coded feedback for towers and enemies.

## Features
- CLI-based gameplay with ASCII map
- Three tower types: AOE, Long Range, Slow
- Enemies scale in health and number each wave
- Color-coded map: green for towers, red for enemies, blue for placement
- End-of-wave map state for planning
- Money and health system

## Requirements
- Python 3.7 or higher
- Works on Linux, macOS, and Windows (with ANSI color support)

## How to Run
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd TTT
   ```
2. **Run the game:**
   ```bash
   python3 -m game.run_game
   ```

## How to Play
- **Menu:**
  - Buy towers, adjust settings (future), or start a wave.
- **Buying Towers:**
  - Choose a tower type, select a valid map coordinate, and confirm placement.
  - Towers cost money; you earn money by damaging enemies.
- **Waves:**
  - Enemies move along the path each turn.
  - Towers attack automatically if in range.
  - If an enemy reaches the end, you lose health.
  - At the end of each wave, the map shows the last enemy positions for planning.
- **Legend:**
  - `O` = path
  - `X` = empty
  - `E` = enemy (red)
  - `A` = AOE Tower (green)
  - `L` = Long Range Tower (green)
  - `S` = Slow Tower (green)
  - Blue = tower placement preview

## Tips
- Place towers off the path for best effect.
- Use the end-of-wave map to plan your next moves.
- Each tower type has unique strengths—experiment!

## License
MIT License

## Disclaimer
This project is intended for educational and research purposes only.
It is not designed or intended for malicious use, and the author does not condone or support any illegal or unethical behavior related to the use of this code.
Use responsibly and in compliance with all applicable laws and regulations.

---
*Created for fun and learning. Pull requests welcome!*
