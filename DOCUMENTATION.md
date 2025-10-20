# Fencing Game – Code Documentation

This document provides an overview of the `fencing_game.py` module, which contains the main class and logic for a fencing-themed game using ASCII art animations and a basic AI opponent.

---

## Table of Contents

- [Module Overview](#module-overview)
- [Classes](#classes)
  - [FencingGame](#class-fencinggame)
    - [Attributes](#attributes)
    - [Methods](#methods)
    - [Static Methods](#static-methods)
    - [Constants](#constants)
- [Functions](#functions)
  - [main()](#main)
- [Data](#data)

---

## Module Overview

- **File:** `fencing_game.py`
- **Purpose:** Implements the GUI, game mechanics, move logic, and AI for a fencing game.
- **GUI Library:** `tkinter`

---

## Classes

### Class `FencingGame`

Handles the main logic of the fencing game with ASCII art animations and an AI opponent.

---

#### Attributes

| Name                     | Type     | Description                                             |
|--------------------------|----------|---------------------------------------------------------|
| `root`                   | `tk.Tk`  | The main Tkinter window                                 |
| `ANIMATION_DELAY`        | `int`    | Milliseconds delay between animation frames             |
| `TARGET_ASCII_HEIGHT`    | `int`    | Target height for ASCII art blocks                      |
| `TARGET_ASCII_WIDTH`     | `int`    | Target width for ASCII art blocks                       |
| `ascii_sequences`        | `dict`   | Mapping of move names to ASCII animation frame names    |
| `moves`                  | `dict`   | Dictionary of allowed counters per move                 |
| `moves_with_feint`       | `list`   | Moves that can be feinted                               |
| `personality_risk_map`   | `dict`   | Risk levels by AI personality                           |

---

#### Methods

##### `__init__(self, root)`
Initializes the FencingGame with the given root window.

- **Parameters:**
  - `root (tk.Tk)`: The main Tkinter window.

---

##### `setup_ui(self)`
Sets up the GUI layout using `tkinter` widgets including ASCII art display, input fields, and overlays.

---

##### `on_submit(self, event=None)`
Handles the user's move submission via the input field.

- **Parameters:**
  - `event`: Optional tkinter event (e.g., Return key press).

---

##### `input_check(self, move)`
Validates the user's move based on game logic.

- **Parameters:**
  - `move (str)`: The user's input move.

- **Returns:**  
  - `"Invalid input"`  
  - `"Loss for user - Invalid counter"`  
  - `"Loss for user - Parrying a feint"`  
  - `None` (if valid)

---

##### `choose_computer_move(self, user_move)`
Determines the computer’s next move based on AI strategy and the user’s last move.

- **Parameters:**
  - `user_move (str)`: The user’s last move.

- **Returns:**  
  `str`: The selected move by the computer.

---

##### `fatigue_factor(self)`
Calculates a fatigue effect that reduces predictability over time.

- **Returns:**  
  `float`: Fatigue factor (minimum of `0.2`)

---

##### `update_ascii_art(self, move, animation_delay=500)`
Displays the ASCII animation for a given move.

- **Parameters:**
  - `move (str)`: Move string like `"User-Lunge"` or `"Computer-Parry-Riposte"`.
  - `animation_delay (int)`: Delay in milliseconds between animation frames.

---

##### `restart_game(self)`
Resets game state, GUI fields, and selects a new computer personality.

---

##### `end_game(self)`
Handles game over UI and displays the move history and result.

---

#### Static Methods

##### `align_ascii_block(art, target_height=18, target_width=50, shift_right=False)`
Aligns and optionally shifts an ASCII art block within the given dimensions.

- **Parameters:**
  - `art (str)`: The ASCII art string.
  - `target_height (int)`: Target height for the block.
  - `target_width (int)`: Target width for the block.
  - `shift_right (bool)`: Whether to align right.

- **Returns:**  
  `str`: Aligned ASCII art block.

---

## Functions

### `main()`

Starts the application by creating a Tkinter window, instantiating the `FencingGame`, and entering the main event loop.

---

## Data

These constants and data structures are defined at the module or class level.

---

### Constants

- `TARGET_ASCII_HEIGHT = 18`
- `TARGET_ASCII_WIDTH = 50`
- `ANIMATION_DELAY = 500`

---

### Class-level Data

- `moves`: Dictionary defining valid counters for each move.
- `moves_with_feint`: List of moves eligible to be feinted.
- `ascii_sequences`: Maps move names to a sequence of ASCII art frames.
- `personality_risk_map`: Personality types mapped to risk-taking likelihood.

---

## Notes

- ASCII art frames are stored in `ascii_art_storage.py`.
- The game AI uses basic rule-based prediction and "feint" mechanics.
- The game is built entirely with `tkinter` and does not require external dependencies.
