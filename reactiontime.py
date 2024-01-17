import pyautogui
import mss
import webbrowser
import time

def get_pixel_color(x,y):
    with mss.mss() as sct:
        bbox =(x,y,x+1,y+1)
        # Grab the data
        sct_img = sct.grab(bbox)
        return sct_img.rgb

x = 1422 #Change to x coordinate of a pixel within the game
y = 312 #Change to y coordinate of a pixel within the game

webbrowser.open('https://humanbenchmark.com/tests/reactiontime', new=2)
time.sleep(1)
pyautogui.click(x, y)

for i in range(0,5):
    while True:
        color = get_pixel_color(x,y)
        r, g, b = color[0], color[1], color[2]
        #Once pixel is green it clicks
        if(g > 100 and r < 200 and b < 200):
            pyautogui.click(clicks=2)
            break