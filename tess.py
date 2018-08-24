from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps
import pytesseract
import os

def img_to_sudoku():
    """
    assumes the_play.clean_image has run
    iterates through all 81 cells saved by clean_image and extracts text from them
    if text is a number from 1-9, adds that to nested list puzzle
    if not, uses 0 as a placeholder for empty
    WILL NOT WORK if tesseract is not installed. pytesseract is only a package to interact with tesseract.
    """
    sudoku = []
    for i in range(9):
        row = []
        for j in range(9):
            img = PIL.ImageOps.invert(Image.open(f"temp/cell row{i} col{j}.jpg"))
            val = pytesseract.image_to_string(img, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789")
            # psm 10 tells tesseract to look for single characters. whitelist is BROKEN IN TESSERACT 4. consider switching to 3.
            if val == '' or val not in "123456789":
                row.append(0)
            else:
                row.append(int(val))
            os.remove(f"temp/cell row{i} col{j}.jpg")

        sudoku.append(row)
    return sudoku