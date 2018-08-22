from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps
import pytesseract
import argparse
import cv2
import os
import numpy as np

sudoku = []
for i in range(9):
    row = []
    #instantiates row
    for j in range(9):
        img = PIL.ImageOps.invert(Image.open(f"celltest row{i} col{j}.jpg"))
        # loops through cell files saved in the_play
        # pytesseract needs pil format, unfortunately.
        val = pytesseract.image_to_string(img, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789")
        # psm 10 tells tesseract to look for single characters. whitelist IS BROKEN IN TESSERACT 4
        # Cheap whitelist replacement
        if val == '' or val not in "123456789":
            row.append(0)
            # if cell is empty populates row with placeholder 0
        else:
            row.append(int(val))
            # populates row with found number

    sudoku.append(row)
    # adds row to full puzzle
for each in sudoku:
    print(each)