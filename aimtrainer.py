import numpy as np
import cv2
from mss import mss
import pyautogui
import webbrowser
import time

pyautogui.PAUSE = 0.00
pyautogui.MINIMUM_DURATION = 0.00

bounding_box = {'top': 142, 'left': 502, 'width': 1555-502, 'height': 638-142} #Change to be the bounding box of the game

sct = mss()

def detect_white_regions(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold to identify white regions
    _, thresholded = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(thresholded, (9, 9), 2)

    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=30,
        maxRadius=100
    )
    
    # Get coordinates of the centers of detected circles
    coordinates = []
    if circles is not None:
        for circle in circles[0, :]:
            x, y = int(circle[0]), int(circle[1])
            coordinates.append((x, y))
            
    # If circles are found, draw them on the original image
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            
            # Draw the circle
            #cv2.circle(image, center, radius, (0, 255, 0), 2)
            cv2.circle(image, center, radius, 255, thickness=cv2.FILLED)

    
    return image, coordinates

coords = []
count = 0
levels = 60
webbrowser.open('https://humanbenchmark.com/tests/aim', new=2)
time.sleep(1)
pyautogui.click(953, 391)

while count < levels:
    sct_img = sct.grab(bounding_box)
    img = np.array(sct_img)
    white, coords = detect_white_regions(img)
    
    if(coords):
        for c in coords:
            pyautogui.click(c[0]+502,c[1]+142) #Change these magic numbers to be equal to whatever the bounding box top and left are
            break
        count += 1    
    
    