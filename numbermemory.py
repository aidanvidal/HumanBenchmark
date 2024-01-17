#Still bugging, code is not reading the numbers 1,6,9 on the first level
#I think it has something to do with pytesseract.image_to_string
import cv2
import pytesseract
import mss
import numpy as np
import webbrowser
import time
import pyautogui

sct = mss.mss()

bounding_box = {'top': 333, 'left': 453, 'width': 1450-453, 'height': 429-333} #Change to be the bounding box of the game

def extract_numbers(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold to create a binary image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 5) #Try changing the block size

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    numbers = []

    # Iterate through contours
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Crop the region containing the number
        number_region = img[y:y + h, x:x + w]

        # Use Tesseract to perform OCR on the cropped region
        text = pytesseract.image_to_string(number_region, config='--psm 10 --oem 3')

        # Extracted text might contain noise; filter only numeric characters
        number = ''.join(char for char in text if char.isdigit())

        if number:
            numbers.append(int(number))

    return numbers

prev = 0
levels = 5
count = 0

webbrowser.open('https://humanbenchmark.com/tests/number-memory', new=2)
time.sleep(1)
pyautogui.click(947,535)

try:
    while count < levels:
        # Grab the image
        sct_img = sct.grab(bounding_box)
        img = np.array(sct_img)
        numbers = extract_numbers(img)
        # Check if numbers is empty
        if numbers:
            prev = numbers[0]
        # If numbers is empty, then prev is the answer
        elif prev != 0:
            time.sleep(0.5)
            pyautogui.write(str(prev))
            time.sleep(0.5)
            pyautogui.press('enter', presses=2)
            count += 1 
except KeyboardInterrupt:
    print('Done')
    