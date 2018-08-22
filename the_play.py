from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

img = cv2.imread("sudoku_clean.png",0)
blur = cv2.bilateralFilter(img,9,75,75) #bilateral is probably best for my purposes. blurs like colored sections to reduce noise, but maintains border integrity

# size grabs size of image, size//1200 determined through experimentation to give best results
# adaptiveThreshold() used below requires sample size to be odd.
sample = blur.size//1200
if sample % 2 == 0:
    sample += 1
elif sample < 11:
    sample = 11

# adaptive threshold applies value based one darker/lighter {sample} nearby pixels
# thresh_binary converts pixel from greyscale to pure black/white based on adaptive values
blur2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,sample ,2)

# countours becomes list of all found contours (solid line shapes)
# POTENTIAL ISSUE: current format assumes that borders will be contained inside photo. system does not function if image cuts any borders off (should be a non issue
contoured, contours, hierarchy = cv2.findContours(blur2,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

area = 0
# checks how far the lines of a contour shape warp, and if they're within epsilon boundaries, simplifies them. basically converts a badly drawn square to square
for cnt in contours:
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    # assumes sudoku puzzle is the largest single contour in the image.
    if cv2.contourArea(cnt) > area:
        area = cv2.contourArea(approx)
        puzzle = approx

pts1=np.float32(puzzle)
pts2=np.float32([[0,0],[0,315],[315,315],[315,0]])
m = cv2.getPerspectiveTransform(pts1,pts2)
t = cv2.warpPerspective(blur2,m,(315,315))
# uses corners of found puzzle contour to adjust angled/distorted puzzle into corrected square

for col in range(9):
    for row in range(9):
        cv2.imwrite(f'celltest row{row} col{col}.jpg', t[row*35+5:(row+1)*35-3,col*35+5:(col+1)*35-3])

# iterates through all cells of puzzle and saves all cell contents with row/col index
# per remapping conditions,each cell is 35px*35px. row*35+5:row+1*35-3 grab only contents, not borders. borders screwed up text recognition
