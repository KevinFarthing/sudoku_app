from sudoku_solver import sudoku_solver, validSolution
from clean_image import clean_image
from tess import img_to_sudoku
import cv2
import time

# total runtime: 54.4 seconds
# sudoku solver runtime : 5.5 seconds
# yikes.
start_time = time.time()

img = cv2.imread("capture.jpeg",0)

clean_image(img)
puzzle = img_to_sudoku()

print("extracted puzzle:")
for each in puzzle:
    print(each)

solved = sudoku_solver(puzzle)

sudoku_solver_start_time = time.time()

print("solved puzzle:")
for each in solved:
    print(each)

print(validSolution(solved))

end_time = time.time()

print(f'total runtime: {end_time-sudoku_solver_start_time} seconds')