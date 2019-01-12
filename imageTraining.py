import numpy as np
from PIL import ImageGrab
import cv2
from time import sleep

sleep(3)
for i in range(100):
    ss = np.array(ImageGrab.grab())
    ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
    resized_ss = cv2.resize(ss, (100, 100))
    cv2.imwrite("negative_images/" + str(i) + ".jpg", resized_ss)
    sleep(0.5)
