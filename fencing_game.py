import random
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import ttk
from ascii_art_storage import ascii_art

class FencingGame:
    """
    Class for a fencing game with ASCII art animations and AI opponent.

    Attributes:
        root (tk.Tk): The main Tkinter window.
    """
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

    ascii_sequences = {
        "Garde": ["Garde"],
        "Lunge": ["Lunge"],
        "Fleche": ["Fleche"],
        "Stophit": ["Stretch"],
        "Marche-Lunge": ["Marche", "Garde", "Lunge"],
        "Distance": ["Garde", "Rompe", "Garde", "Lunge"],
        "Parry-Riposte": ["Parry", "Stretch"],
        "Redoublement": ["Garde", "Lunge"],
    }

    personality_risk_map = {
        "Aggressive": 0.6,
        "Defensive": 0.2,
        "Unpredictable": 0.4
    }

    TARGET_ASCII_WIDTH = 50
    TARGET_ASCII_HEIGHT = 18
    ANIMATION_DELAY = 500

    def __init__(self, root):
        """
        Initialize the FencingGame with the main Tkinter window.

        Parameters:
            root (tk.Tk): The main Tkinter window. 
        """
        self.root = root
        self.root.title("Fencing Game")
        self.computer_personality = None
        self.user_moves = []
        self.computer_moves = []
        self.user_transitions = defaultdict(Counter)
        self.winner = None
        self.why_loss = None

        # UI elements placeholders
        self.entry_user = None
        self.entry_computer_output = None
        self.text_user_ascii = None
        self.text_computer_ascii = None
        self.listbox = None
        self.overlay = None
        self.label = None

        self.setup_ui()
        self.restart_game()

    @staticmethod
    def align_ascii_block(art, target_height=TARGET_ASCII_HEIGHT, target_width=TARGET_ASCII_WIDTH, shift_right=False):
        """
        Align ASCII art block to target dimensions.
        
        Parameters:
            art (str): The ASCII art string.
            target_height (int): The target height for the ASCII art block.
            target_width (int): The target width for the ASCII art block.
            shift_right (bool): Whether to shift the art to the right.

        Returns:
            str: The aligned ASCII art block.
        """
        lines = art.strip('\n').splitlines()
        max_line_length = max(len(line) for line in lines)
        if shift_right:
            space_needed = target_width - max_line_length
            horizontal_padding = " " * max(space_needed, 0)
            lines = [horizontal_padding + line for line in lines]
        missing_lines = target_height - len(lines)
        if missing_lines > 0:
            top_padding = [""] * missing_lines
            lines = top_padding + lines
        return "\n".join(lines)

    def update_ascii_art(self, move, animation_delay=ANIMATION_DELAY):
        """
        Update the ASCII art display with animation for the given move.
        
        Parameters:
            move (str): The move to animate (e.g., "User-Lunge", "Computer-Parry-Riposte").
            animation_delay (int): Delay in milliseconds between animation frames.
        """
        # Determine who moves
        who = "User" if "User" in move else "Computer"
        who_moves = self.user_moves if who == "User" else self.computer_moves
        box = self.text_user_ascii if who == "User" else self.text_computer_ascii

        # Frames sequence
        base_move = move.replace(f"{who}-", "").replace("Feint-", "")
        frames = self.ascii_sequences[base_move]

        box.config(state="normal")
        box.delete("1.0", tk.END)

        # If repeated move, blank first for animation reset
        if len(who_moves) >= 2 and who_moves[-1].replace("Feint-", "") == who_moves[-2].replace("Feint-", ""):
            box.insert("1.0", "\n" * 18)
            box.update_idletasks()

        def make_insert_func(pos, target_box):
            def insert_art():
                target_box.delete("1.0", tk.END)
                key = f"{who}-{pos}"
                if who == "Computer":
                    target_box.insert(tk.END, self.align_ascii_block(ascii_art[key], shift_right=True))
                else:
                    target_box.insert(tk.END, self.align_ascii_block(ascii_art[key]))
            return insert_art

        # Animation timing
        if len(who_moves) >= 2 and who_moves[-1].replace("Feint-", "") == who_moves[-2].replace("Feint-", ""):
            for i, position in enumerate(frames):
                self.root.after(300 + animation_delay * i, make_insert_func(position, box))
            self.root.after(300 + animation_delay * len(frames), lambda: box.config(state="disabled"))
        else:
            for i, position in enumerate(frames):
                self.root.after(animation_delay * i, make_insert_func(position, box))
            self.root.after(animation_delay * len(frames), lambda: box.config(state="disabled"))

    def setup_ui(self):
        """
        Set up the Tkinter UI elements.
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.text_user_ascii = tk.Text(frame, bd=0, highlightthickness=0, height=20, width=50, font=("Courier", 12))
        self.text_computer_ascii = tk.Text(frame, bd=0, highlightthickness=0, height=20, width=50, font=("Courier", 12))
        self.text_user_ascii.pack(side=tk.LEFT)
        self.text_computer_ascii.pack(side=tk.LEFT)

        frame_text = tk.Frame(self.root)
        frame_text.pack(pady=10)

        self.entry_user = tk.Entry(frame_text, width=30)
        self.entry_user.pack(side=tk.LEFT, padx=5)

        self.entry_computer_output = tk.Entry(frame_text, width=30, fg="black", state="readonly")
        self.entry_computer_output.pack(side=tk.LEFT, padx=5)

        self.entry_user.bind("<Return>", self.on_submit)
        self.entry_user.focus_set()

        self.overlay = tk.Toplevel(self.root)
        self.overlay.title("Game Over")
        self.overlay.geometry("800x400")
        self.overlay.transient(self.root)
        x = screen_width // 2 - 400
        y = screen_height // 2 - 200
        self.overlay.geometry(f"+{x}+{y}")

        self.label = tk.Label(self.overlay, text="Placeholder", font=("Helvetica", 14), pady=20)
        self.label.pack(expand=True)

        result_frame = tk.Frame(self.overlay)
        result_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        self.listbox = tk.Listbox(result_frame, height=10, width=10)
        self.listbox.pack(side=tk.TOP, anchor="center")

        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT)
        self.listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(result_frame)
        button_frame.pack(side=tk.TOP, anchor="center", padx=10, pady=10)

        restart_button = tk.Button(button_frame, text="Restart Game", command=self.restart_game)
        restart_button.pack(side=tk.LEFT, pady=10)
        quit_button = tk.Button(button_frame, text="Quit", command=self.root.quit)
        quit_button.pack(side=tk.LEFT, pady=10)

        self.overlay.withdraw()
        self.overlay.attributes("-topmost", False)

    def input_check(self, move):
        """
        Check the validity of the user's input move.
        
        Parameters:
            move (str): The user's input move.
            
        Returns:
            str: "Invalid input" if the move is invalid,
                 "Loss for user - Invalid counter" if the move cannot counter the computer's last move,
                 "Loss for user - Parrying a feint" if the user parries a feint,
                 None if the move is valid.
        """
        move = move.strip().title()
        if move not in self.moves and not move.startswith("Feint"):
            return "Invalid input"
        if self.computer_moves:
            last_comp = self.computer_moves[-1].replace("Feint-", "")
            if move not in self.moves[last_comp] and not move.startswith("Feint"):
                return "Loss for user - Invalid counter"
            if self.computer_moves[-1].startswith("Feint") and move == "Parry-Riposte":
                return "Loss for user - Parrying a feint"

    def fatigue_factor(self):
        """
        Calculate the fatigue factor based on the number of user moves.
        
        Returns:
            float: The fatigue factor, minimum of 0.2.
        """
        return max(0.2, 1.0 - len(self.user_moves) * 0.05)

    def choose_computer_move(self, user_move):
        """
        Choose the computer's move based on the user's last move and game state.

        Parameters:
            user_move (str): The user's last move.

        Returns:
            str: The chosen computer move.
        """
        potential_moves = self.moves[user_move]
        best_move = None
        best_score = -1
        risk_taking = self.personality_risk_map[self.computer_personality]

        recent_user_moves = self.user_moves[-3:] if len(self.user_moves) >= 3 else self.user_moves
        if recent_user_moves:
            likely_recent = Counter(recent_user_moves).most_common(1)[0][0]
            if likely_recent in potential_moves and random.random() < 0.4:
                return likely_recent

        if random.random() > self.fatigue_factor():
            return random.choice(potential_moves)

        if random.random() < risk_taking:
            feintable = [m for m in potential_moves if m in self.moves_with_feint]
            if feintable:
                return "Feint-" + random.choice(feintable)

        for candidate in potential_moves:
            counters = self.user_transitions.get(candidate, Counter())
            if not counters:
                continue

            predicted = random.choices(population=list(counters.keys()), weights=list(counters.values()))[0]

            if predicted == "Parry-Riposte" and candidate in self.moves_with_feint:
                candidate = "Feint-" + candidate

            score = counters[predicted]
            if score > best_score:
                best_score = score
                best_move = candidate

        if len(self.user_moves) >= 2 and len(self.computer_moves) >= 2:
            if ((self.user_moves[-1].replace("Feint-", "") == self.user_moves[-2].replace("Feint-", "") and
                self.computer_moves[-1].replace("Feint-", "") == self.computer_moves[-2].replace("Feint-", ""))
                or self.computer_moves[-1].replace("Feint-", "") == self.computer_moves[-2].replace("Feint-", "")):
                last_move = self.computer_moves[-1].replace("Feint-", "")
                filtered_moves = [m for m in potential_moves if m != last_move]
                if filtered_moves:
                    return random.choice(filtered_moves)

        if best_move:
            return best_move
        else:
            return random.choice(potential_moves)

    def on_submit(self, event=None):
        """
        Handle the user's move submission.
        
        Parameters:
            event: The Tkinter event (not used).
        """
        user_input = self.entry_user.get()
        self.entry_user.delete(0, tk.END)

        result = self.input_check(user_input)
        if result == "Invalid input":
            self.listbox.insert(tk.END, f"Invalid input: {user_input}")
            return
        elif result == "Loss for user - Invalid counter":
            self.winner = "Computer"
            self.why_loss = "Invalid counter"
            self.user_moves.append(user_input)
            self.end_game()
            return
        elif result == "Loss for user - Parrying a feint":
            self.winner = "Computer"
            self.why_loss = "Parrying a feint"
            self.user_moves.append(user_input)
            self.end_game()
            return

        self.user_moves.append(user_input)
        self.update_ascii_art("User-" + user_input.replace("Feint-", ""))

        if len(self.user_moves) >= 2:
            starter = self.computer_moves[-1]
            reaction = self.user_moves[-1]
            self.user_transitions[starter][reaction] += 1

        user_move_b = user_input.replace("Feint-", "") if user_input.startswith("Feint") else user_input
        computer_move_b = self.choose_computer_move(user_move_b)
        computer_move = computer_move_b.replace("Feint-", "") if computer_move_b.startswith("Feint") else computer_move_b

        if user_input.startswith("Feint") and computer_move_b == "Parry-Riposte":
            self.winner = "User"
            self.computer_moves.append(computer_move_b)
            self.end_game()
            return

        self.computer_moves.append(computer_move_b)

        # Show computer's move and animation after 500ms
        self.entry_computer_output.config(state="normal")
        self.entry_computer_output.delete(0, tk.END)
        self.root.after(500, lambda: self.entry_computer_output.insert(0, computer_move))
        self.root.after(500, lambda: self.entry_computer_output.config(state="readonly"))
        self.root.after(500, lambda: self.update_ascii_art("Computer-" + computer_move))

    def restart_game(self):
        """
        Restart the game by resetting all relevant attributes and UI elements.
        """
        self.user_moves.clear()
        self.computer_moves.clear()
        self.user_transitions.clear()
        self.winner = None
        self.why_loss = None

        self.overlay.grab_release()
        self.overlay.withdraw()
        self.overlay.attributes("-topmost", False)

        self.entry_user.config(state="normal")
        self.entry_user.delete(0, tk.END)
        self.entry_user.focus_set()

        self.entry_computer_output.config(state="normal")
        self.entry_computer_output.delete(0, tk.END)
        self.entry_computer_output.config(state="readonly")

        self.text_user_ascii.config(state="normal")
        self.text_user_ascii.delete("1.0", tk.END)
        self.text_user_ascii.insert(tk.END, self.align_ascii_block(ascii_art["User-Garde"]))
        self.text_user_ascii.config(state="disabled")

        self.text_computer_ascii.config(state="normal")
        self.text_computer_ascii.delete("1.0", tk.END)
        self.text_computer_ascii.insert(tk.END, self.align_ascii_block(ascii_art["Computer-Garde"], shift_right=True))
        self.text_computer_ascii.config(state="disabled")

        self.listbox.config(state="normal")
        self.listbox.delete(0, tk.END)
        self.listbox.config(state="disabled")

        self.computer_personality = random.choice(list(self.personality_risk_map.keys()))

    def end_game(self):
        """
        Handle the end of the game, displaying results and final moves.
        """
        self.overlay.deiconify()
        self.overlay.grab_set()
        self.overlay.lift()

        if self.winner == "User":
            text = "win!"
        else:
            if self.why_loss == "Invalid counter":
                text = f"lose :(\n{self.user_moves[-1]} cannot counter {self.computer_moves[-1]}"
            else:
                text = f"lose :(\nYou fell for the computer's feint"

        self.label.config(text=f"You {text}")

        final_moves_list = []

        if len(self.user_moves) == len(self.computer_moves):
            for i in range(len(self.user_moves)):
                final_moves_list.append(f"{i+1}> {self.user_moves[i]}:{self.computer_moves[i]}")
        else:
            for i in range(len(self.user_moves)-1):
                final_moves_list.append(f"{i+1}> {self.user_moves[i]}:{self.computer_moves[i]}")
            final_moves_list.append(f"{len(self.user_moves)}> {self.user_moves[-1]}:--")

        final_moves_length = len(max(final_moves_list, key=len)) + 2

        self.listbox.config(state="normal")
        self.listbox.config(width=final_moves_length)

        for item in final_moves_list:
            self.listbox.insert(tk.END, item)

def main():
    """
    Main function to run the FencingGame.
    """
    root = tk.Tk()
    game = FencingGame(root)
    game.computer_personality = random.choice(list(game.personality_risk_map.keys()))
    game.update_ascii_art("User-Garde")
    game.update_ascii_art("Computer-Garde")
    game.root.after(100, lambda: game.entry_user.focus_set())
    game.root.mainloop()

if __name__ == "__main__":
    main()
