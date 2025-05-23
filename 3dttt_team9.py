import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

# Constants
GRID_SIZE = 4
PLAYER = 1
AI = 2
EASY, DIFFICULT, INSANE = 2, 4, 6

# Initialize board
def create_board():
    return np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=int)

# Generate all winning lines in 3D Tic Tac Toe
def winning_lines():
    lines = []
    SIZE = GRID_SIZE

    for z in range(SIZE):
        for y in range(SIZE):
            lines.append([(z, y, x) for x in range(SIZE)])
        for x in range(SIZE):
            lines.append([(z, y, x) for y in range(SIZE)])
        lines.append([(z, i, i) for i in range(SIZE)])
        lines.append([(z, i, SIZE - 1 - i) for i in range(SIZE)])

    for y in range(SIZE):
        for x in range(SIZE):
            lines.append([(z, y, x) for z in range(SIZE)])

    for x in range(SIZE):
        lines.append([(i, i, x) for i in range(SIZE)])
        lines.append([(i, SIZE - 1 - i, x) for i in range(SIZE)])

    for y in range(SIZE):
        lines.append([(i, y, i) for i in range(SIZE)])
        lines.append([(i, y, SIZE - 1 - i) for i in range(SIZE)])

    lines.append([(i, i, i) for i in range(SIZE)])
    lines.append([(i, i, SIZE - 1 - i) for i in range(SIZE)])
    lines.append([(i, SIZE - 1 - i, i) for i in range(SIZE)])
    lines.append([(i, SIZE - 1 - i, SIZE - 1 - i) for i in range(SIZE)])

    return lines

WINNING_COMBINATIONS = winning_lines()

# Check if a player has won
def has_won(board, player):
    return next((line for line in WINNING_COMBINATIONS if all(board[z][y][x] == player for z, y, x in line)), None)

# Return available moves
def available_moves(board):
    return [(z, y, x) for z in range(GRID_SIZE) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if board[z][y][x] == 0]

# Minimax with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing):
    if has_won(board, AI):
        return 10 - depth
    if has_won(board, PLAYER):
        return depth - 10
    if not available_moves(board) or depth == 0:
        return 0

    if maximizing:
        max_eval = -float('inf')
        for z, y, x in available_moves(board):
            board[z][y][x] = AI
            eval = minimax(board, depth - 1, alpha, beta, False)
            board[z][y][x] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for z, y, x in available_moves(board):
            board[z][y][x] = PLAYER
            eval = minimax(board, depth - 1, alpha, beta, True)
            board[z][y][x] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Get best move using full minimax for Insane, hybrid for others
def get_best_move(board, depth):
    move_scores = []
    for z, y, x in available_moves(board):
        board[z][y][x] = AI
        score = minimax(board, depth - 1, -float('inf'), float('inf'), False)
        board[z][y][x] = 0
        move_scores.append(((z, y, x), score))

    move_scores.sort(key=lambda x: x[1], reverse=True)
    return move_scores[0][0] if move_scores else random.choice(available_moves(board))

# Game UI class
class ThreeDTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Tic Tac Toe")
        self.root.configure(bg='#121225')
        self.board = create_board()
        self.current_turn = PLAYER
        self.difficulty = None
        self.buttons = [[[None]*GRID_SIZE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.setup_ui()

    def setup_ui(self):
        top = tk.Frame(self.root, bg='#121225')
        top.pack(pady=10)

        self.play_btn = tk.Button(top, text="PLAY", command=self.start_game, state=tk.DISABLED, bg='#292947', fg='cyan')
        self.play_btn.grid(row=0, column=0, padx=5)
        tk.Button(top, text="RESET", command=self.reset_game, bg='#292947', fg='cyan').grid(row=0, column=1, padx=5)
        tk.Button(top, text="RULES", command=self.show_rules, bg='#292947', fg='cyan').grid(row=0, column=2, padx=5)

        diff = tk.Frame(self.root, bg='#121225')
        diff.pack(pady=5)
        tk.Button(diff, text="Easy", command=lambda: self.set_difficulty(EASY), bg='#292947', fg='cyan').grid(row=0, column=0, padx=5)
        tk.Button(diff, text="Difficult", command=lambda: self.set_difficulty(DIFFICULT), bg='#292947', fg='cyan').grid(row=0, column=1, padx=5)
        tk.Button(diff, text="Insane", command=lambda: self.set_difficulty(INSANE), bg='#292947', fg='cyan').grid(row=0, column=2, padx=5)

        self.status = tk.Label(self.root, text="Select Difficulty", font=("Arial", 14), bg='#121225', fg='white')
        self.status.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg='#121225')
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg='#121225')

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        for z in range(GRID_SIZE):
            layer = tk.LabelFrame(self.scroll_frame, text=f"Layer {z + 1}", bg='#121225', fg='cyan', font=("Arial", 12, "bold"))
            layer.pack(pady=10)
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    btn = tk.Button(layer, text="", width=4, height=2, font=("Arial", 16), bg='#292947', fg='white',
                                    command=lambda z=z, y=y, x=x: self.player_move(z, y, x))
                    btn.grid(row=y, column=x, padx=2, pady=2)
                    self.buttons[z][y][x] = btn

    def set_difficulty(self, level):
        self.difficulty = level
        self.play_btn.config(state=tk.NORMAL)
        self.status.config(text="Press Play to Start")

    def start_game(self):
        self.reset_game()
        self.status.config(text="Your Turn (X)")

    def player_move(self, z, y, x):
        if self.difficulty is None:
            messagebox.showwarning("Warning", "Please select a difficulty.")
            return
        if self.board[z][y][x] == 0 and self.current_turn == PLAYER:
            self.board[z][y][x] = PLAYER
            self.update_button(z, y, x, 'X')
            if self.check_victory(PLAYER):
                return
            self.current_turn = AI
            self.status.config(text="AI's Turn (O)")
            self.root.after(300, self.ai_turn)

    def ai_turn(self):
        depth = {EASY: 1, DIFFICULT: 2, INSANE: 4}[self.difficulty]
        move = get_best_move(self.board, depth)
        if move:
            z, y, x = move
            self.board[z][y][x] = AI
            self.update_button(z, y, x, 'O')
            if self.check_victory(AI):
                return
        self.current_turn = PLAYER
        self.status.config(text="Your Turn (X)")

    def update_button(self, z, y, x, symbol):
        self.buttons[z][y][x].config(text=symbol, state='disabled', fg='cyan' if symbol == 'X' else 'magenta')

    def check_victory(self, player):
        line = has_won(self.board, player)
        if line:
            for z, y, x in line:
                self.buttons[z][y][x].config(bg='green' if player == PLAYER else 'red', fg='white')
            messagebox.showinfo("Game Over", "You Win!" if player == PLAYER else "AI Wins!")
            return True
        if not available_moves(self.board):
            messagebox.showinfo("Game Over", "It's a Draw!")
            return True
        return False

    def reset_game(self):
        self.board = create_board()
        for z in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    self.buttons[z][y][x].config(text="", state="normal", bg="#292947", fg="white")
        self.current_turn = PLAYER
        self.status.config(text="Your Turn (X)")

    def show_rules(self):
        rules = ("Rules:\n"
                 "1. Play on a 4x4x4 grid.\n"
                 "2. Get 4 in a row in any direction to win.\n"
                 "3. Select difficulty and press PLAY.")
        messagebox.showinfo("Game Rules", rules)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    ThreeDTicTacToe(root)
    root.mainloop()
