import numpy as np
import turtle
from time import sleep

puzzle_grid = np.array([   [3,0,6,5,0,8,4,0,0],
                               [5,2,0,0,0,0,0,0,0],
                               [0,8,7,0,0,0,0,3,1],
                               [0,0,3,0,1,0,0,8,0],
                               [9,0,0,8,6,3,0,0,5],
                               [0,5,0,0,9,0,6,0,0],
                               [1,3,0,0,0,0,2,5,0],
                               [0,0,0,0,0,0,0,7,4],
                               [0,0,5,2,0,6,3,0,0]])

def main():
    print_puzzle()
    solve()

def solve():
    global puzzle_grid
    for row, i in enumerate(puzzle_grid):
        for column, j in enumerate(i):
            if j==0:
                for candidate in range(1,10):
                    if possible(candidate, row, column):
                        puzzle_grid[row,column]=candidate
                        solve()
                        puzzle_grid[row,column]=0 # backtrack if recursion failed
                return
    print("Done, solved puzzle:")
    print_puzzle()

def possible(candidate, row, column):
    global puzzle_grid
    #check 3x3 grid
    for i in range(row-row%3, row-row%3+3):
        for j in range(column-column%3, column-column%3+3):
            if candidate==puzzle_grid[i][j]:
                return False
    #check row
    for j in range(9):
        if candidate==puzzle_grid[row][j]:
                return False
    #check column
    for i in range(9):
        if candidate==puzzle_grid[i][column]:
                return False
    return True
        
def print_puzzle():
    global puzzle_grid
    for row, i in enumerate(puzzle_grid):
        if row%3==0:
            print("\n-----------------------------------------")
        else:
           print("")
        for column, j in enumerate(i):
            number = '-' if j==0 else j
            if column==len(i)-1:
                print("|", number, "||", end =" ")
            elif column%3==0:
                print("||", number, end =" ")
            else:
                print("|", number, end =" ")
    print("\n-----------------------------------------")

if __name__=="__main__":
    main()