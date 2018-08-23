from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps
import pytesseract
import argparse
import cv2
import os
import numpy as np

def img_to_sudoku():
    """
    assumes the_play.clean_image has run
    iterates through all 81 cells saved by clean_image and extracts text from them
    if text is a number from 1-9, adds that to nested list puzzle
    if not, uses 0 as a placeholder for empty
    """
    sudoku = []
    for i in range(9):
        row = []
        for j in range(9):
            img = PIL.ImageOps.invert(Image.open(f"cell row{i} col{j}.jpg"))
            val = pytesseract.image_to_string(img, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789")
            # psm 10 tells tesseract to look for single characters. whitelist IS BROKEN IN TESSERACT 4
            if val == '' or val not in "123456789":
                row.append(0)
            else:
                row.append(int(val))

        sudoku.append(row)
    for each in sudoku:
        print(each)