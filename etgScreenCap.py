import numpy as np
from PIL import ImageGrab
import cv2
from win32 import win32gui
import time

hwnd = win32gui.FindWindow(None, "Enter the Gungeon")
x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
w = x1 - x0
h = y1 - y0
win32gui.MoveWindow(hwnd, 0, 0, w, h, False)

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    vertices = np.array([[160, 160], [640, 160], [640, 480], [160, 480]])
    processed_img = roi(processed_img, [vertices])

    return processed_img

last_time = time.time()
while(True):
    screen =  np.array(ImageGrab.grab(bbox=(10, 30, 800, 630)))
    new_screen = process_img(screen)
    
    #print('Loop took {} seconds'.format(time.time()-last_time))
    last_time = time.time()
    cv2.imshow('window', new_screen)
    #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
