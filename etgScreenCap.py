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

move_window()
bullet_cascade = cv2.CascadeClassifier('bullet_cascade.xml')
last_time = time.time()
while(True):
    screen =  np.array(ImageGrab.grab(bbox=(10, 30, 800, 630)))
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    bullets = bullet_cascade.detectMultiScale(screen)

    for (x,y,w,h) in bullets:
        cv2.rectangle(screen, (x,y), (x+w, y+h), (255,255,0), 2)
        #print("Got one!")
        
    #print('Loop took {} seconds'.format(time.time()-last_time))
    last_time = time.time()
    cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
