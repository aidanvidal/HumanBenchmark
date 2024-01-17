import pyautogui
import pytesseract
from PIL import ImageGrab
import webbrowser
import time
    
    
board_top_left = (792, 352) #Board dimensions
board_bottom_right = (1125, 419) #Board dimensions
words_seen = (893, 471) #Change to where to click if word is seen
words_new = (1031, 476) #Change to where to click if word is new
lvls = 50 #Number of levels
all_Words = []

webbrowser.open('https://humanbenchmark.com/tests/verbal-memory', new=2)
time.sleep(1)
pyautogui.click(949, 553)


for i in range(0,lvls):
    bbox = (board_top_left[0],board_top_left[1],board_bottom_right[0],board_bottom_right[1])
    img = ImageGrab.grab(bbox=bbox)
    word = pytesseract.image_to_string(img)
    if word not in all_Words:
        all_Words.append(word)
        pyautogui.click(words_new[0],words_new[1])
    else:
        pyautogui.click(words_seen[0],words_seen[1])