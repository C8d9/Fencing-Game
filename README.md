# Fencing Game

**Fencing Game** is a turn-based, ASCII-animated fencing simulator built with Python and Tkinter. The game features a ruleset inspired by real fencing strategies, reactive AI opponents with varied personalities, and feint mechanics to simulate psychological gameplay. All movements are visualized with ASCII animations for both the user and the computer opponent.

---

## Documentation

See [documentation](DOCUMENTATION.md)

## Features

- **Reactive AI**: Opponents simulate different personalities (Aggressive, Defensive, Unpredictable) and adapt to player behavior.
- **Feint Mechanics**: Users can bluff with `Feint-<Move>` and bait the AI into reacting incorrectly.
- **Game Outcome Logic**: The game ends when the user makes an invalid counter or falls for a feint.

---

## Gameplay

Players enter one fencing move at a time in a GUI input field. The computer responds based on internal prediction logic. Each move is animated in a dedicated ASCII canvas.

### Valid Moves

| Move           | Can Be Feinted | Possible Counters                               |
|----------------|----------------|--------------------------------------------------|
| Lunge          | Yes            | Parry-Riposte, Stophit, Distance                 |
| Marche-Lunge   | Yes            | Parry-Riposte, Stophit, Distance                 |
| Fleche         | No             | Parry-Riposte                                    |
| Parry-Riposte  | Yes            | Parry-Riposte, Stophit, Distance, Redoublement  |
| Stophit        | Yes            | Parry-Riposte, Stophit                           |
| Distance       | Yes            | Redoublement, Parry-Riposte, Stophit            |
| Redoublement   | Yes            | Parry-Riposte, Stophit, Distance                 |

Feints are entered using the syntax:

Feint-Move

### Fencing Logic

The valid counters to moves are based on this logic tree of epee fencing. In this logic tree, "distance" means to pull out the distance with a rompé and then counterattack (here with a lunge).

![Logic of fencing](https://github.com/user-attachments/assets/fd2841c2-fea7-4f85-b0c2-44f6257167ee)

This logic is stored like so inside the project:
```bash
moves = {
        "Lunge": ["Parry-Riposte", "Stophit", "Distance"],
        "Marche-Lunge": ["Parry-Riposte", "Stophit", "Distance"],
        "Fleche": ["Parry-Riposte"],
        "Parry-Riposte": ["Parry-Riposte", "Stophit", "Distance", "Redoublement"],
        "Stophit": ["Parry-Riposte", "Stophit"],
        "Distance": ["Redoublement", "Distance", "Parry-Riposte", "Stophit"],
        "Redoublement": ["Parry-Riposte", "Stophit", "Distance"]
    }

moves_with_feint = ["Lunge", "Marche-Lunge", "Stophit", "Distance", "Redoublement", "Parry-Riposte"]
```

#### Changes to fencing logic for gameplay

- Reprise has not been implemented because it is almost like a redoublement, making no change to the gameplay.
- Although it is possible to do stophits etc. against fleche, it is generally wisest to do parry-riposte, since stophits against fleche are quite difficult and risky.
- Because only parry-riposte is counted as a valid move against fleche, feinting with a fleche is not allowed because that would make it unstoppable. I am aware that this is not realistic, but I had to make the gameplay work.

### Limitations

- At a certain level, fencing is no longer about following the above-mentioned logic, because everyone knows it. Being able to use this against the opponent by strategically break against the logic to surprise them becomes important. 
- Fencing is also never completely about this strategic tree alone. A very imortant factor is when and how a move is performed. This has not been simulated because that would turn this from a strategic game into a reaction-based fighting game.
- Different parries and target areas have not been implemented because, although they are important in fencing, they are still fundamentally the same, although they are used is slightly different situations, none of them are ever, technically, wrong.
- I am aware that it would be very awkward to fence according to the matches simulated in the game because most moves don't flow smoothly into each other. In a real match, moves would be altered based on the situation, but that is not strictly necessary for thi game and has thus not been added.

### Game Ends If:

- The player chooses an invalid counter for the opponent’s last move.
- The player parries a feint (i.e., uses `Parry-Riposte` against a feint).

The user wins if the computer falls for a feint and attempts to parry.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Tkinter (included with most Python distributions)

### Clone and Run

```bash
git clone https://github.com/<your-github-username>/fencing-game.git
cd fencing-game
python fencing_game.py
```

## Project Structure
```bash
fencing-game/
├── fencing_game.py           # Main game logic and GUI
├── ascii_art_storage.py      # Contains all ASCII art frames
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
```

## License
This project is licensed under the MIT License (see [here](LICENSE.md)).
