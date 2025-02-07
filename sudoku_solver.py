from collections import defaultdict
from typing import List, Tuple
from copy import deepcopy
import time


class Solver:
    def __init__(self) -> None:
        self.rows = defaultdict(set)
        self.cols = defaultdict(set)
        self.boxes = defaultdict(set)
        self.board = [[0 for i in range(9)] for i in range(9)]

    def sudoku_solver(self, input_board: List[List[int]]) -> List[List[int]]:
        self.board = deepcopy(input_board)

        # Place existing numbers to the gird
        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                if val != 0:
                    self.rows[r].add(val)
                    self.cols[c].add(val)
                    self.boxes[(r // 3, c // 3)].add(val)

        self.backtrack(0, 0)
        # Return the original input board if the sudoku board is not valid
        if self.board != input_board:
            return self.board
        else:
            return input_board

        # Check if a number can be placed according to the constraints

    def can_place_number(self, r: int, c: int, num: int) -> bool:
        if (
            (num in self.rows[r])
            or (num in self.cols[c])
            or (num in self.boxes[(r // 3, c // 3)])
        ):
            return False
        else:
            return True

    def place_number_in_cell(self, r: int, c: int, num: int) -> None:
        self.board[r][c] = num
        self.rows[r].add(num)
        self.cols[c].add(num)
        self.boxes[(r // 3, c // 3)].add(num)

    def remove_number_in_cell(self, r: int, c: int, num: int) -> None:
        self.board[r][c] = 0
        self.rows[r].remove(num)
        self.cols[c].remove(num)
        self.boxes[(r // 3, c // 3)].remove(num)

    def move_to_next_cell(self, r: int, c: int) -> Tuple[int, int]:
        # Move to next column
        if c < 8:
            return r, c + 1
        # Move to next row, reset column index
        else:
            return r + 1, 0

    def backtrack(self, r: int, c: int) -> bool:
        # Base case: reached last row + 1
        if r > 8:
            return True

        # If a number already existed in the cell, move to the next cell
        if self.board[r][c] != 0:
            new_r, new_c = self.move_to_next_cell(r, c)
            return self.backtrack(new_r, new_c)

        # If a number can be placed, place it to the board
        for num in range(1, 10):
            if self.can_place_number(r, c, num):
                self.place_number_in_cell(r, c, num)
                if self.backtrack(r, c):
                    return True
                else:
                    self.remove_number_in_cell(r, c, num)

        # The sudoku is not solvable
        return False


if __name__ == "__main__":
    INPUT_BOARD = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    def print_board(board: List[List[int]]) -> None:
        board_copy = deepcopy(board)
        board_copy = [[str(num) for num in row] for row in board_copy]
        for i, arr in enumerate(board_copy):
            for j, num in enumerate(arr):
                board_copy[i][j] = str(num)

        print("-" * 25)
        for i, row in enumerate(board_copy):
            for j, num in enumerate(row):
                if num == "0":
                    row[j] = "."
            row_str = " | ".join(
                [" ".join(map(str, row[m : m + 3])) for m in range(0, len(row), 3)]
            )
            print(f"| {row_str} |")
            if (i + 1) % 3 == 0:
                print("-" * 25)

    print("\nGiven:")
    print_board(INPUT_BOARD)

    # Solve the Sudoku board
    start_time = time.time()
    solution = Solver().sudoku_solver(INPUT_BOARD)
    print(f"\nTime taken in milliseconds: {(time.time() - start_time) * 1000 :.2f}")

    if solution != INPUT_BOARD:
        print("\nSolution:")
        print_board(solution)
    else:
        print("\nNot a valid Sudoku board.")
