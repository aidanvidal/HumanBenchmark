import cv2
import pytesseract
import numpy as np
import mss
import webbrowser
import time
import pyautogui

bounding_box = {'top': 134, 'left': 523, 'width': 1427-523, 'height': 615-134} # Change these values to match the game border

sct = mss.mss()

def extract_text(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold to create a binary image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 8)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_numbers = []
    
    # Iterate through contours
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        if(w < 20):
            continue

        # Crop the region containing the text
        text_region = img[y:y + h, x:x + w]

        # Use Tesseract OCR to extract text from the region
        result = pytesseract.image_to_string(text_region, config='--psm 10 --oem 3')
        
        if(not result.strip().isdigit()): # Pytesseract sometimes detects a letter instead of the number 9
            result = '9\n'
               
        # Store the detected number and its location
        detected_numbers.append({
            'number': int(result),
            'location': (x+w/2, y+h/2)
        })
    
    return detected_numbers

levels = 25
count = 0
webbrowser.open('https://www.humanbenchmark.com/tests/chimp')
time.sleep(1)
pyautogui.click(956, 542)
time.sleep(1)

while count < levels:
    # Capture the screen within the given bounding box
    img = np.array(sct.grab(bounding_box))

    # Draw rectangles around the numbers and extract text
    detected_numbers = extract_text(img)
    
    if(detected_numbers):
        count += 1
        sort = sorted(detected_numbers, key=lambda k: k['number'])
        for s in sort:
            print(s['number'])
            pyautogui.click(s['location'][0]+523, s['location'][1]+134) # Change these values to match the game border, top and left
        print("count: " + str(count))
        pyautogui.click(956, 536)
        time.sleep(0.1)

        