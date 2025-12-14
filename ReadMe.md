# Connect 4 AI Game
<img src="connect 4.png">

## Overview

This project implements a classic **Connect 4** game in Python, featuring a graphical user interface (GUI) built with Tkinter. The game allows a human player (using red pieces) to compete against an AI opponent (using yellow pieces). The AI uses the **Minimax algorithm with Alpha-Beta Pruning** to make strategic decisions, ensuring challenging gameplay.

The board is a 6x7 grid, and the goal is to connect 4 pieces in a row, column, or diagonal. The AI's decision-making depth is set to 3 by default but can be adjusted for difficulty.

Key features:
- Gravity-based piece dropping.
- Win detection in horizontal, vertical, and diagonal directions.
- Heuristic evaluation for AI moves, including center column bonuses and threat blocking.
- Simple GUI with restart functionality.
- Game ends with win, loss, or draw notifications.

## Requirements

- Python 3.x
- Tkinter (included in standard Python installations)
- Additional modules: `math`, `random`, `copy` (all standard library)

No external libraries are required beyond what's in the standard Python distribution.

## Installation

1. Clone or download the repository.
2. Ensure Python is installed on your system.
3. Run the script directly (no installation needed).

## How to Run

Execute the Python script:

```bash
python3 AiProject.py
```

- Click on a column to drop your piece (red).
- The AI (yellow) will respond automatically.
- Use the "Restart Game" button to start over.

## Code Structure

The code is divided into logical sections:

1. **Board Class**: Manages the game board, piece dropping, removal, and valid moves.
2. **Win Checking and Window Evaluation**: Functions to detect wins and score board windows for heuristics.
3. **Position Scoring**: Heuristic evaluation of the board state, including center bonuses and threat assessments.
4. **Minimax Algorithm**: Recursive search for optimal moves with alpha-beta pruning.
5. **GUI Class**: Handles the Tkinter interface, drawing, user input, and AI turns.

### Key Components
- **Minimax Depth**: Adjustable in `MinimaxAgent(depth=3)`. Higher depths make AI stronger but slower.
- **Scoring Constants**: Tune values like `SCORE_FOUR`, `SCORE_THREE` for custom AI behavior.
- **Heuristics**: Prioritizes center control and blocking opponent threats.

## Limitations
- AI depth is limited to prevent long computation times.
- No multiplayer mode (human vs. human).
- Basic GUI without animations or sound.