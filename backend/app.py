from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import copy
import random

app = Flask(__name__)
CORS(app)  # Allow React frontend to access this API

# -------- Sudoku Generator Helpers -------- #

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_board(board, visualize_callback=None):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        
                        # If a callback is provided, invoke it with the current board state
                        if visualize_callback:
                            visualize_callback(board)
                        
                        if solve_board(board, visualize_callback):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_board(board)
    return board

def remove_cells(board, level="easy"):
    puzzle = copy.deepcopy(board)
    difficulty = {
        "easy": 30,
        "medium": 40,
        "hard": 50
    }
    cells_to_remove = difficulty.get(level, 30)
    count = 0
    while count < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    return puzzle

# -------- API Routes -------- #

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", puzzle=None, solved=None, steps=None)

@app.route("/generate", methods=["POST"])
def generate():
    full_board = generate_full_board()
    puzzle = remove_cells(full_board, level="easy")
    return render_template("index.html", puzzle=puzzle, solved=None, steps=None)

@app.route("/solve", methods=["POST"])
def solve():
    puzzle = generate_full_board()
    puzzle = remove_cells(puzzle, level="easy")
    solution = copy.deepcopy(puzzle)
    solve_board(solution)
    return render_template("index.html", puzzle=puzzle, solved=solution, steps=None)

@app.route("/visualize", methods=["POST"])
def visualize():
    puzzle = generate_full_board()
    puzzle = remove_cells(puzzle, level="easy")

    steps = []

    # This will store each snapshot of the board during solving
    def visualize_callback(grid_snapshot):
        steps.append(copy.deepcopy(grid_snapshot))

    board_copy = copy.deepcopy(puzzle)
    solve_board(board_copy, visualize_callback=visualize_callback)

    return render_template("index.html", puzzle=puzzle, solved=None, steps=steps)

if __name__ == "__main__":
    app.run(debug=True)
