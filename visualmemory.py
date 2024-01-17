import cv2
import numpy as np
from mss import mss
import time
import pyautogui
import webbrowser

bounding_box = {'top': 216, 'left': 448, 'width': 1131, 'height': 450} #Change to be the bounding box of the game

sct = mss()

def detect_and_draw_white_squares(input_image):
 
    # Convert the image to grayscale
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment white regions
    _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store center coordinates of detected squares
    centers = []

    # Draw detected squares on the image
    detected_image = input_image.copy()

    for contour in contours:
        # Approximate the contour into a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Filter squares based on the number of vertices
        if len(approx) == 4:
            # Calculate the center coordinates
            center = np.mean(approx, axis=0, dtype=np.int32)[0]

            # Append center coordinates to the list
            centers.append(tuple(center))

            # Draw the square and center on the image
            cv2.polylines(detected_image, [approx], True, (0, 255, 0), 2)
            cv2.circle(detected_image, tuple(center), 5, (255, 0, 0), -1)

    return centers, detected_image


coords = []
prev_coords = []
count = 0
levels = 10 #Change to be the number of levels you want to play

webbrowser.open('https://humanbenchmark.com/tests/memory', new=2)
time.sleep(1)
pyautogui.click(951, 524) #Change these magic numbers to be equal to where the start box is
time.sleep(1.5)

while count < levels:
    #Grab the image
    sct_img = sct.grab(bounding_box)
    img = np.array(sct_img)
    prev_coords = coords
    coords, img = detect_and_draw_white_squares(img)
    
    if(not coords and prev_coords):
        for c in prev_coords:
            pyautogui.click(c[0]+448,c[1]+216) #Change these magic numbers to be equal to whatever the bounding box top and left are
        time.sleep(2)
        count += 1    