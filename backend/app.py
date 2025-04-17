from flask import Flask, jsonify, request
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

def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
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

@app.route("/")
def hello():
    return jsonify({"message": "Hello from Flask!"})

# Generate puzzle
@app.route("/api/generate", methods=["GET"])
def generate_puzzle():
    full_board = generate_full_board()
    puzzle = remove_cells(full_board, level="easy")  # Change level later
    return jsonify({"puzzle": puzzle})

# Solve puzzle
@app.route("/api/solve", methods=["POST"])
def solve_puzzle():
    puzzle = request.json.get("puzzle")
    if puzzle:
        solved_board = copy.deepcopy(puzzle)
        solve_board(solved_board)
        return jsonify({"solution": solved_board})
    return jsonify({"error": "No puzzle provided"}), 400

# Visualize solving process
@app.route("/api/visualize", methods=["POST"])
def visualize_solving():
    puzzle = request.json.get("puzzle")
    if puzzle:
        steps = []  # List to store intermediate steps
        puzzle_copy = copy.deepcopy(puzzle)
        
        def record_step():
            steps.append([row[:] for row in puzzle_copy])  # Make a snapshot of the current state
        
        # Modified solve_board to record steps
        def solve_with_steps(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                record_step()
                                if solve_with_steps(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        solve_with_steps(puzzle_copy)
        return jsonify({"visualization": steps})
    
    return jsonify({"error": "No puzzle provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
