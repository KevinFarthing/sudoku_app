from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

img = cv2.imread("sudoku_clean.png",0)
blur = cv2.bilateralFilter(img,9,75,75) #bilateral is probably best for my purposes

sample = blur.size//1200
if sample % 2 == 0:
    sample += 1
elif sample < 11:
    sample = 11

blur2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,sample ,2)

contoured, contours, hierarchy = cv2.findContours(blur2,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
 
area = 0
for cnt in contours:
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    if cv2.contourArea(cnt) > area:
        area = cv2.contourArea(approx)
        puzzle = approx

pts1=np.float32(puzzle)
pts2=np.float32([[0,0],[0,315],[315,315],[315,0]])
m = cv2.getPerspectiveTransform(pts1,pts2)
t = cv2.warpPerspective(blur2,m,(315,315))

cv2.imshow("test",t)

cv2.waitKey(0)
cv2.destroyAllWindows()

for col in range(9):
    for row in range(9):
        cv2.imwrite(f'celltest row{row} col{col}.jpg', t[row*35+5:(row+1)*35-3,col*35+5:(col+1)*35-3])

