import cv2
import time
import numpy as np
from win32 import win32gui
from PIL import ImageGrab

def move_window():
    hwnd = win32gui.FindWindow(None, "Enter the Gungeon")
    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    w = x1 - x0
    h = y1 - y0
    win32gui.MoveWindow(hwnd, 0, 0, w, h, False)

def locate_bullets(original_img):
    gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    
    # run template matching, get minimum val
    res = cv2.matchTemplate(gray, bullet, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # create threshold from min val, find where sqdiff is less than thresh
    min_thresh = (min_val + 1e-6) * 1.2
    match_locations = np.where(res<=min_thresh)

    # draw template match boxes
    w, h = bullet.shape[::-1]
    for (x, y) in zip(match_locations[1], match_locations[0]):
        cv2.rectangle(original_img, (x, y), (x+w, y+h), [0,255,255], 2)

def capture_screen():
    bullet_cascade = cv2.CascadeClassifier('bullet_cascade.xml')
    last_time = time.time()
    while(True):
        screen = np.array(ImageGrab.grab(bbox=(10, 30, 1280, 750)))
        #locate_bullets(screen)
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        bullets = bullet_cascade.detectMultiScale(screen, 10, 10)

        for (x,y,w,h) in bullets:
            cv2.rectangle(screen, (x,y), (x+w, y+h), (255,255,0), 2)
        #print("Got one!")   
        #print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    
bullet = cv2.imread('bullet5050.jpg', 0)
move_window()
capture_screen()
