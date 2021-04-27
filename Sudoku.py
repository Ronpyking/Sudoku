import numpy as np
import tkinter as tk
import random

class Sudoku:
    def __init__(self):
        self.grid = self.Generate()

    def Generate(self):
        def NewGrid():
            grid = np.zeros((9, 9)).astype(int)
            return grid

        grid = NewGrid()
        while self.CountEmpty(grid) != 0:
            for i in range(9):
                for j in range(9):
                    possible_entries = []
                    for value in range(1, 10):
                        if self.PossibilityCheck(grid, value, i, j): 
                            possible_entries.append(value)
                    if len(possible_entries) == 0:
                        grid = NewGrid()
                    else:
                        random_possible = random.choice(possible_entries)
                        grid[i, j] = random_possible

        while self.Solve(grid)[1]:
            initial_sudoku = np.copy(grid)
            grid[random.randint(0, 8), random.randint(0, 8)] = 0

        return initial_sudoku

    def Solve(self, grid):
        """Try to solve the sudoku or deem it unsolvable"""
        solved_grid = np.copy(grid)
        is_solvable = True
        while self.CountEmpty(solved_grid) != 0 and is_solvable:
            empty_fields = self.CountEmpty(solved_grid)
            possible_values_grid = np.empty((9, 9), dtype=object)
            for i in range(9):
                for j in range(9):
                    possible_values_grid[i][j] = []

            for value in range(1, 10):
                for i in range(9):
                    for j in range(9):
                        if self.PossibilityCheck(solved_grid, value, i, j):
                            possible_values_grid[i, j].append(value)

            for i in range(9):
                for j in range(9):
                    if len(possible_values_grid[i, j]) == 1:
                        solved_grid[i, j] = possible_values_grid[i, j].pop()

            if empty_fields == self.CountEmpty(solved_grid):
                is_solvable = False

        return solved_grid, is_solvable

    def Display(self):
        window = tk.Tk()
        for i in range(9):
            row_frame = tk.Frame(master=window)
            for j in range(9):
                tk.Label(text=str(self.grid[i, j]) if self.grid[i, j] != 0 else " ", master=row_frame,\
                    width=4, height=2, relief="solid", font=("Arial", 15)).pack(side=tk.LEFT)
            row_frame.pack(side=tk.TOP)
        window.mainloop()

    @staticmethod
    def PossibilityCheck(grid, val, row, col):
        """Returns true if the value is possible on that spot of the grid, false otherwise"""
        
        is_empty = grid[row, col] == 0
        row_missing = val not in grid[row, :]
        column_missing = val not in grid[:, col]
        sub_i, sub_j = row//3, col//3

        sqr_missing = True
        for k in range(3):
            for h in range(3):
                if grid[sub_i * 3 + k, sub_j * 3 + h] == val: sqr_missing = False

        return is_empty and row_missing and column_missing and sqr_missing

    @staticmethod
    def CountEmpty(grid):
        """Return the number of empty fields"""
        return grid.size - np.count_nonzero(grid)

sudoku = Sudoku()
sudoku.Display()
sudoku.grid = sudoku.Solve(sudoku.grid)[0]
sudoku.Display()
