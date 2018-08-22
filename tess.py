from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps
import pytesseract
import argparse
import cv2
import os
import numpy as np

# # img = Image.open("celltest row0 col5.jpg")
# img = PIL.ImageOps.invert(Image.open("celltest row2 col6.jpg"))
# # img.show()

# text = pytesseract.image_to_string(img, config="--psm 10")
# print("celltest found :" + text +": and no more")
# answers{'03':'1','05':'4','06':'8','21':'2','22':'1','26':'9','28':'7','33':'3','34':'1','36':'7','40':'9','43':'8','48':'6','50':'8', '54':'5','55':'2','60':'2','62':'7','66':'1','67':'8','82':'5','83':'6','85':'9','86':'2'}
sudoku = []
for i in range(9):
    row = []
    for j in range(9):
        img = PIL.ImageOps.invert(Image.open(f"celltest row{i} col{j}.jpg"))
        val = pytesseract.image_to_string(img, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789")
        if val == '' or val not in "123456789":
            row.append(0)
        else:
            row.append(int(val))
        # crap, interprets 1 as 4. probably border related. also one time 9 as E.
        # interprets 9 as g on 26
    sudoku.append(row)
for each in sudoku:
    print(each)