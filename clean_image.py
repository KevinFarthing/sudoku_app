from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

# img = cv2.imread("/test_image/capture.jpeg",0)

def clean_image(img):
    """given image, uses cv2 to reduce noise using bilateral filter
    converts to pure B/W with dynamically generated adaptive thresholding samples
    remaps image using contour detection to find puzzle corners in image
    splits image into 81 individual cells saved in static/images
    ASSUMPTION:
    photo contains space beyond borders of puzzle. if not, it inhibits contour detection
    converts image so each cell is 35x35. assumes 5px on each side of cell contain only borders, and no relevent data.
    """
    blur = cv2.bilateralFilter(img,9,75,75)

    sample = blur.size//1200
    if sample % 2 == 0:
        sample += 1
    elif sample < 11:
        sample = 11

    blur2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,sample ,2)

    # POTENTIAL ISSUE: current format assumes that borders will be contained inside photo. system does not function if image cuts any borders off (should be a non issue
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

    for col in range(9):
        for row in range(9):
            cv2.imwrite(f'temp/cell row{row} col{col}.jpg', t[row*35+5:(row+1)*35-3,col*35+5:(col+1)*35-3])