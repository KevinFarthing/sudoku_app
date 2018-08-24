from copy import deepcopy
import numpy as np
easy_base = [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]


 
def validSolution(board):
    board = np.array(board)
    for i in range(9):
        if board[i].sum() != 45 or board[:,i].sum() != 45 or board[i%3*3:((i%3)+1)*3,i//3*3:(i//3+1)*3].sum() != 45:
            return False
    return True
 
 
solved_board = []
def sudoku_solver(board):
    def is_full(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False
        return True
   
    def possible_entries(board, i, j):
        possibility_array={}
        for x in range(1,10):
            possibility_array[x] = 0
        for y in range(9):
            if board[i][y] != 0:
                possibility_array[board[i][y]] = 1
        for x in range(9):
            if board[x][j] != 0:
                possibility_array[board[x][j]] = 1
        k = i//3 * 3
        l = j//3 * 3
        for x in range(k, k+3):
            for y in range(l,l+3):
                if board[x][y] != 0:
                    possibility_array[board[x][y]]=1
        for x in range(1,10):
            if possibility_array[x]==0:
                possibility_array[x]=x
            else:
                possibility_array[x]=0
        return possibility_array
   
    def sudoku_solver(board):
        i = 0
        j = 0
        possibilities = {}
        if is_full(board):
            global solved_board
            solved_board = deepcopy(board)
        else:
            for x in range(9):
                for y in range(9):
                    if board[x][y]==0:
                        i,j=x,y
                        break
                    else:
                        continue
                    break
            possibilities = possible_entries(board, i, j)
            for x in range(1,10):
                if possibilities[x] != 0:
                    board[i][j] = possibilities[x]
                    sudoku_solver(board)
            board[i][j] = 0
    sudoku_solver(board)
    return solved_board

# test = solve(easy_base)
# print(test)
# print(validSolution(test))