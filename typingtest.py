#Pytesseract detects the upper case 'I' as a lower case 'l'
import re
import pyautogui
from PIL import ImageGrab
import pytesseract
import time
import webbrowser

webbrowser.open('https://humanbenchmark.com/tests/typing', new=2)
time.sleep(1)

top_left = (464,357) #Change to be the top left of the typing box
bottom_right = (1443, 533) #Change to be the bottom right of the typing box

bbox = (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
img = ImageGrab.grab(bbox=bbox)
words = pytesseract.image_to_string(img)
words = re.sub(r'\s+', ' ', words).strip()
pyautogui.write(words)
print(words)