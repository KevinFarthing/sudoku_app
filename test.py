from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import argparse
import cv2
import os
import numpy as np

img = PIL.ImageOps.invert(Image.open(f"temp/celltest row{i} col{j}.jpg"))
val = pytesseract.image_to_string(img, config="--psm 10 --oem 3 -c tessedit_char_whitelist=123456789")