import time
import pyautogui
import mss
import webbrowser

def get_pixel_color(x,y):
    with mss.mss() as sct:
        bbox =(x,y,x+1,y+1)
        # Grab the data
        sct_img = sct.grab(bbox)
        return sct_img.rgb

def compute_positions(top_left,bottom_right):
    width = (bottom_right[0]-top_left[0]) // 2
    height = (bottom_right[1]-top_left[1]) // 2

    positions_ = [
        (top_left[0], top_left[1]),
        (top_left[0] + width, top_left[1]),
        (bottom_right[0], top_left[1]),
        (top_left[0], top_left[1]+height),
        (top_left[0]+width,top_left[1]+height),
        (bottom_right[0],top_left[1]+height),
        (top_left[0],bottom_right[1]),
        (top_left[0]+width,bottom_right[1]),
        (bottom_right[0],bottom_right[1])
    ]
    return positions_

top_left = (814,288) #Change to be the middle of the top left block
bottom_right = (1089,560) #Change to be the middle of the bottom right block
flash_list = []
last_flash_time = None
levels = 10 #Change to the number of levels you want to play
count = 0

webbrowser.open('https://humanbenchmark.com/tests/sequence', new=2)
time.sleep(1)
pyautogui.click(953, 522)
positions = compute_positions(top_left,bottom_right)

try:
    while count < levels:
        for i, pos in enumerate(positions):
            color = get_pixel_color(pos[0],pos[1])
            r, g, b = color[0], color[1], color[2]
            #If the pixel is white, add it to the list
            if r == 255 and g == 255 and b == 255:
                #Check if the flash is already in the list, if not add it
                if len(flash_list) == 0 or flash_list[-1] != i:
                    flash_list.append(i)
                    last_flash_time = time.time()
        #If the last flash was more than 3 seconds ago, click the flashes
        if last_flash_time and (time.time() - last_flash_time) >= 1:
            for i in flash_list:
                pyautogui.click(positions[i][0],positions[i][1])
            flash_list.clear()
            last_flash_time = None
            count += 1
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nDone.')
       